from django.db import models

from apps.accounts.models import User


class Provider(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )
    business_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name