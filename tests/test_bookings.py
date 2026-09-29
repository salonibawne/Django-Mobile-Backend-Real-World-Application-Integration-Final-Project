import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.bookings.models import Booking
from apps.providers.models import Provider
from apps.services.models import Service


@pytest.mark.django_db
def test_booking_list():
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username="customer@example.com",
        email="customer@example.com",
        password="Test@123",
    )

    provider = Provider.objects.create(
        user=user,
        business_name="Test Services",
        phone="9876543210",
        address="Test Address",
        city="Nagpur",
    )

    service = Service.objects.create(
        provider=provider,
        name="Home Cleaning",
        description="Test cleaning service",
        price=500,
        is_available=True,
    )

    Booking.objects.create(
        customer=user,
        service=service,
        booking_date="2026-09-25T10:00:00Z",
        status="PENDING",
        notes="Test booking",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/bookings/")

    assert response.status_code == 200