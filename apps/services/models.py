from django.db import models

from apps.providers.models import Provider


class Service(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="services"
    )

    name = models.CharField(max_length=150)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class ServiceImage(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="services/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.service.name} - Image {self.id}"