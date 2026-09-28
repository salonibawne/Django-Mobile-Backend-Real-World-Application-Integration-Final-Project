
from django.db import models
from apps.accounts.models import User


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        BOOKING_CREATED = "BOOKING_CREATED", "Booking Created"
        PAYMENT_SUCCESS = "PAYMENT_SUCCESS", "Payment Successful"
        BOOKING_CONFIRMED = "BOOKING_CONFIRMED", "Booking Confirmed"
        BOOKING_STARTED = "BOOKING_STARTED", "Provider Started Service"
        BOOKING_COMPLETED = "BOOKING_COMPLETED", "Booking Completed"
        BOOKING_CANCELLED = "BOOKING_CANCELLED", "Booking Cancelled"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
