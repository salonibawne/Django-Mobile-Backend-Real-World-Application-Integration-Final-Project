import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.services.models import Service
from apps.providers.models import Provider


@pytest.mark.django_db
class TestAuthorizationAudit:

    def setup_method(self):
        self.client = APIClient()

        self.customer = User.objects.create_user(
            username="customer@example.com",
            email="customer@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

        self.provider_user = User.objects.create_user(
            username="provider@example.com",
            email="provider@example.com",
            password="TestPassword123!",
            role="PROVIDER",
        )

        self.provider = Provider.objects.create(
            user=self.provider_user,
            business_name="Test Provider",
            phone="9876543210",
            address="Test Address",
            city="Nagpur",
        )
        self.service = Service.objects.create(
            provider=self.provider,
            name="Test Service",
            description="Test service",
            price=500,
        )

        self.booking = Booking.objects.create(
            customer=self.customer,
            service=self.service,
            booking_date="2026-10-01T10:00:00Z",
            status="PENDING",
        )

    def test_anonymous_cannot_access_bookings(self):
        response = self.client.get("/api/v1/bookings/")
        assert response.status_code == 401

    def test_customer_cannot_confirm_booking(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.patch(
            f"/api/v1/bookings/{self.booking.id}/confirm/",
            {},
            format="json",
        )

        assert response.status_code in [403, 404]

    def test_customer_cannot_complete_booking(self):
        self.client.force_authenticate(user=self.customer)

        response = self.client.patch(
            f"/api/v1/bookings/{self.booking.id}/complete/",
            {},
            format="json",
        )

        assert response.status_code in [403, 404]
    def test_provider_can_confirm_booking(self):
        self.client.force_authenticate(user=self.provider_user)

        response = self.client.patch(
            f"/api/v1/bookings/{self.booking.id}/confirm/",
            {},
            format="json",
        )

        assert response.status_code == 200

    def test_provider_can_complete_booking(self):
        self.client.force_authenticate(user=self.provider_user)

        response = self.client.patch(
            f"/api/v1/bookings/{self.booking.id}/complete/",
            {},
            format="json",
        )

        assert response.status_code == 200