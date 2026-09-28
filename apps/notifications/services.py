
from .models import Notification


def create_notification(
    user,
    notification_type,
    title,
    message,
):
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
    )


def booking_created_notification(booking):
    return create_notification(
        user=booking.customer,
        notification_type=Notification.NotificationType.BOOKING_CREATED,
        title="Booking Created",
        message=(
            f"Your booking for "
            f"{booking.service.name} has been created."
        ),
    )


def payment_success_notification(payment):
    return create_notification(
        user=payment.booking.customer,
        notification_type=Notification.NotificationType.PAYMENT_SUCCESS,
        title="Payment Successful",
        message=(
            f"Payment of ₹{payment.amount} was successful "
            f"for booking #{payment.booking.id}."
        ),
    )


def booking_confirmed_notification(booking):
    return create_notification(
        user=booking.customer,
        notification_type=Notification.NotificationType.BOOKING_CONFIRMED,
        title="Booking Confirmed",
        message=(
            f"Your booking for "
            f"{booking.service.name} has been confirmed."
        ),
    )


def booking_started_notification(booking):
    return create_notification(
        user=booking.customer,
        notification_type=Notification.NotificationType.BOOKING_STARTED,
        title="Service Started",
        message=(
            f"The provider has started your "
            f"{booking.service.name} service."
        ),
    )


def booking_completed_notification(booking):
    return create_notification(
        user=booking.customer,
        notification_type=Notification.NotificationType.BOOKING_COMPLETED,
        title="Booking Completed",
        message=(
            f"Your booking for "
            f"{booking.service.name} has been completed."
        ),
    )


def booking_cancelled_notification(booking):
    return create_notification(
        user=booking.customer,
        notification_type=Notification.NotificationType.BOOKING_CANCELLED,
        title="Booking Cancelled",
        message=(
            f"Your booking for "
            f"{booking.service.name} has been cancelled."
        ),
    )
