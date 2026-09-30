import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.providers.models import Provider
from apps.services.models import Service


@pytest.mark.django_db
class TestThrottlingAudit:

    def setup_method(self):
        cache.clear()

        self.client = APIClient()

        self.user = User.objects.create_user(
            username="throttle@example.com",
            email="throttle@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

    def test_login_throttling(self):
        responses = []

        for _ in range(10):
            response = self.client.post(
                "/api/v1/auth/login/",
                {
                    "username": "throttle@example.com",
                    "password": "WrongPassword123!",
                },
                format="json",
            )

            responses.append(response.status_code)

        assert 429 in responses

    def test_registration_throttling(self):
        responses = []

        for i in range(10):
            response = self.client.post(
                "/api/v1/auth/register/",
                {
                    "email": f"newuser{i}@example.com",
                    "password": "TestPassword123!",
                    "role": "CUSTOMER",
                },
                format="json",
            )

            responses.append(response.status_code)

        assert 429 in responses

    def test_booking_creation_throttling(self):
        provider = Provider.objects.create(
            user=self.user,
            business_name="Throttle Provider",
            phone="9876543210",
            address="Test Address",
            city="Nagpur",
        )

        service = Service.objects.create(
            provider=provider,
            name="Throttle Service",
            description="Test service",
            price=500,
        )

        self.client.force_authenticate(user=self.user)

        responses = []

        for i in range(10):
            response = self.client.post(
                "/api/v1/bookings/",
                {
                    "service": service.id,
                    "booking_date": f"2026-10-{10 + i:02d}T10:00:00Z",
                    "notes": "Throttle test",
                },
                format="json",
            )

            responses.append(response.status_code)

        assert 429 in responses

    def test_payment_initiation_throttling(self):
        provider = Provider.objects.create(
            user=self.user,
            business_name="Payment Provider",
            phone="9876543210",
            address="Test Address",
            city="Nagpur",
        )

        service = Service.objects.create(
            provider=provider,
            name="Payment Service",
            description="Payment throttle test service",
            price=500,
        )

        self.client.force_authenticate(user=self.user)

        responses = []

        for i in range(10):
            booking = Booking.objects.create(
                customer=self.user,
                service=service,
                booking_date=f"2026-11-{10 + i:02d}T10:00:00Z",
                status="PENDING",
            )

            response = self.client.post(
                "/api/v1/payments/initiate/",
                {
                    "booking_id": booking.id,
                },
                format="json",
            )

            responses.append(response.status_code)

        assert 429 in responses