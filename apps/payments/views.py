from decimal import Decimal

from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.notifications.tasks import send_payment_success_notification
from apps.bookings.models import Booking
from apps.common.responses import success_response, error_response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentInitiateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get("booking_id")

        # 1. Booking ID required
        if not booking_id:
            return error_response(
                message="Booking ID is required.",
                error_code="BOOKING_ID_REQUIRED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Check booking exists
        booking = Booking.objects.filter(
            id=booking_id
        ).select_related("service").first()

        if not booking:
            return error_response(
                message="Booking not found.",
                error_code="BOOKING_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # 3. Check booking belongs to logged-in customer
        if booking.customer != request.user:
            return error_response(
                message="You can only make payments for your own bookings.",
                error_code="PAYMENT_BOOKING_FORBIDDEN",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # 4. Check booking status
        if booking.status != Booking.Status.PENDING:
            return error_response(
                message="Only pending bookings can be paid.",
                error_code="BOOKING_NOT_PAYABLE",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # 5. Check existing payment
        if Payment.objects.filter(booking=booking).exists():
            return error_response(
                message="Payment already exists for this booking.",
                error_code="PAYMENT_ALREADY_EXISTS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Amount comes from service price
        amount = Decimal(str(booking.service.price))

        try:
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                transaction_id=(
                    f"MOCK-{booking.id}-{booking.customer.id}"
                ),
                payment_status=Payment.Status.PENDING,
                payment_method=Payment.Method.MOCK,
            )

        except IntegrityError:
            return error_response(
                message="A payment already exists for this booking.",
                error_code="PAYMENT_ALREADY_EXISTS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Payment initiated successfully.",
            data=PaymentSerializer(payment).data,
            status_code=status.HTTP_201_CREATED,
        )


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            booking__customer=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return success_response(
            message="Payments retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            booking__customer=self.request.user
        )

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()

        return success_response(
            message="Payment retrieved successfully.",
            data=self.get_serializer(payment).data,
            status_code=status.HTTP_200_OK,
        )


class PaymentWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        event = request.data.get("event")
        payment_id = request.data.get("payment_id")
        transaction_id = request.data.get("transaction_id")

        # Required fields
        if not event or not payment_id or not transaction_id:
            return error_response(
                message="event, payment_id and transaction_id are required.",
                error_code="PAYMENT_WEBHOOK_FIELDS_REQUIRED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Find payment
        payment = Payment.objects.filter(
            id=payment_id
        ).select_related("booking").first()

        if not payment:
            return error_response(
                message="Payment not found.",
                error_code="PAYMENT_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Payment must be pending
        if payment.payment_status != Payment.Status.PENDING:
            return error_response(
                message="This payment has already been processed.",
                error_code="PAYMENT_ALREADY_PROCESSED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Validate event
        if event == "payment.success":
            payment.payment_status = Payment.Status.SUCCESS

        elif event == "payment.failed":
            payment.payment_status = Payment.Status.FAILED

        else:
            return error_response(
                message="Invalid payment event.",
                error_code="INVALID_PAYMENT_EVENT",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Save gateway transaction ID
        payment.transaction_id = transaction_id

        payment.save(
            update_fields=[
                "payment_status",
                "transaction_id",
            ]
        )
        if payment.payment_status == Payment.Status.SUCCESS:
         send_payment_success_notification.delay(payment.id)
        return success_response(
            message="Payment status updated successfully.",
            data=PaymentSerializer(payment).data,
            status_code=status.HTTP_200_OK,
        )   