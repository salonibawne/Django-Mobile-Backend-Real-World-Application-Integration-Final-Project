
from django.db import models

from apps.accounts.models import User
from apps.services.models import Service


class Booking(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
        PAYMENT_FAILED = "PAYMENT_FAILED", "Payment Failed"

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def change_status(self, new_status):
        allowed_transitions = {
            self.Status.PENDING: {
                self.Status.CONFIRMED,
                self.Status.CANCELLED,
                self.Status.PAYMENT_FAILED,
            },

            self.Status.CONFIRMED: {
                self.Status.IN_PROGRESS,
                self.Status.CANCELLED,
            },

            self.Status.IN_PROGRESS: {
                self.Status.COMPLETED,
            },

            self.Status.COMPLETED: set(),

            self.Status.CANCELLED: set(),

            self.Status.PAYMENT_FAILED: set(),
        }

        if new_status not in self.Status.values:
            raise ValueError("Invalid booking status.")

        if new_status not in allowed_transitions[self.status]:
            raise ValueError(
                f"Invalid transition: {self.status} -> {new_status}"
            )

        self.status = new_status
        self.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    def __str__(self):
        return f"{self.customer.email} - {self.service.name}"
