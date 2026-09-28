from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from .models import Booking
from .serializers import BookingSerializer
from apps.notifications.models import Notification
from apps.common.responses import success_response, error_response


class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            customer=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class BookingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            customer=self.request.user
        )


class BookingCancelView(generics.GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            customer=self.request.user
        )

    def post(self, request, pk):
        booking = self.get_queryset().filter(pk=pk).first()

        if not booking:
            return error_response(
                message="Booking not found.",
                error_code="BOOKING_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if booking.status in [
            Booking.Status.CANCELLED,
            Booking.Status.COMPLETED,
        ]:
            return error_response(
                message="This booking cannot be cancelled.",
                error_code="BOOKING_CANNOT_BE_CANCELLED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CANCELLED
        booking.save()

        Notification.objects.create(
            user=booking.customer,
            notification_type=Notification.NotificationType.BOOKING_CANCELLED,
            title="Booking Cancelled",
            message=f"Your booking #{booking.id} has been cancelled.",
        )

        return success_response(
            message="Booking cancelled successfully.",
            data=BookingSerializer(booking).data,
            status_code=status.HTTP_200_OK,
        )


class BookingConfirmView(generics.GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = Booking.objects.filter(
            pk=pk,
            service__provider__user=request.user,
        ).first()

        if not booking:
            return error_response(
                message="Booking not found.",
                error_code="BOOKING_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if booking.status != Booking.Status.PENDING:
            return error_response(
                message="Only pending bookings can be confirmed.",
                error_code="BOOKING_NOT_PENDING",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.CONFIRMED
        booking.save()

        Notification.objects.create(
            user=booking.customer,
            notification_type=Notification.NotificationType.BOOKING_CONFIRMED,
            title="Booking Confirmed",
            message=f"Your booking #{booking.id} has been confirmed.",
        )

        return success_response(
            message="Booking confirmed successfully.",
            data=BookingSerializer(booking).data,
            status_code=status.HTTP_200_OK,
        )


class BookingCompleteView(generics.GenericAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        booking = Booking.objects.filter(
            pk=pk,
            service__provider__user=request.user,
        ).first()

        if not booking:
            return error_response(
                message="Booking not found.",
                error_code="BOOKING_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if booking.status != Booking.Status.CONFIRMED:
            return error_response(
                message="Only confirmed bookings can be completed.",
                error_code="BOOKING_NOT_CONFIRMED",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        booking.status = Booking.Status.COMPLETED
        booking.save()

        Notification.objects.create(
            user=booking.customer,
            notification_type=Notification.NotificationType.BOOKING_COMPLETED,
            title="Booking Completed",
            message=f"Your booking #{booking.id} has been completed.",
        )

        return success_response(
            message="Booking completed successfully.",
            data=BookingSerializer(booking).data,
            status_code=status.HTTP_200_OK,
        )