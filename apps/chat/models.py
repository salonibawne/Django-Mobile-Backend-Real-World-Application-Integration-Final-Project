from django.db import models

from apps.accounts.models import User
from apps.bookings.models import Booking


class Message(models.Model):

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"