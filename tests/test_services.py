import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.providers.models import Provider
from apps.services.models import Service


@pytest.mark.django_db
def test_service_list():
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username="provider@example.com",
        email="provider@example.com",
        password="Test@123",
    )

    provider = Provider.objects.create(
        user=user,
        business_name="Test Services",
        phone="9876543210",
        address="Test Address",
        city="Nagpur",
    )

    Service.objects.create(
        provider=provider,
        name="Home Cleaning",
        description="Test cleaning service",
        price=500,
        is_available=True,
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/services/")

    assert response.status_code == 200