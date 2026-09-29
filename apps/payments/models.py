from django.db import models

from apps.bookings.models import Booking


class Payment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    class Method(models.TextChoices):
        MOCK = "MOCK", "Mock Payment"

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    payment_method = models.CharField(
        max_length=30,
        choices=Method.choices,
        default=Method.MOCK
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking.id} - {self.payment_status}"