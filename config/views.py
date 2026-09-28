from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            booking__customer=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save()


class PaymentMarkPaidView(generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        payment = Payment.objects.filter(
            pk=pk,
            booking__customer=request.user
        ).first()

        if not payment:
            return Response(
                {"detail": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if payment.status != Payment.Status.PENDING:
            return Response(
                {"detail": "Only pending payments can be marked as paid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = Payment.Status.PAID
        payment.transaction_id = f"TEST-TXN-{payment.id}"
        payment.save()

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_200_OK
        )