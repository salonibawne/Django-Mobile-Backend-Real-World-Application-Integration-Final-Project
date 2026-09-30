import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.services.models import Service
from apps.providers.models import Provider


@pytest.mark.django_db
class TestInputValidationAudit:

    def setup_method(self):
        self.client = APIClient()

        # Customer
        self.customer = User.objects.create_user(
            username="validation_customer@example.com",
            email="validation_customer@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

        # Provider
        self.provider_user = User.objects.create_user(
            username="validation_provider@example.com",
            email="validation_provider@example.com",
            password="TestPassword123!",
            role="PROVIDER",
        )

        self.provider = Provider.objects.create(
            user=self.provider_user,
            business_name="Validation Provider",
            phone="9876543210",
            address="Test Address",
            city="Nagpur",
        )

        # Service
        self.service = Service.objects.create(
            provider=self.provider,
            name="Validation Service",
            description="Service for validation testing",
            price=500,
        )

        self.client.force_authenticate(
            user=self.customer
        )

    # ---------------------------------------------------------
    # 1. Empty booking data
    # ---------------------------------------------------------

    def test_empty_booking_data_rejected(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {},
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 2. Invalid service ID
    # ---------------------------------------------------------

    def test_invalid_service_id_rejected(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "service": "not-a-valid-id",
                "booking_date": "2026-10-01T10:00:00Z",
                "notes": "Test booking",
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 3. Non-existing service ID
    # ---------------------------------------------------------

    def test_non_existing_service_rejected(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "service": 999999,
                "booking_date": "2026-10-01T10:00:00Z",
                "notes": "Test booking",
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 4. Invalid booking date
    # ---------------------------------------------------------

    def test_invalid_booking_date_rejected(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "service": self.service.id,
                "booking_date": "invalid-date",
                "notes": "Test booking",
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 5. Extremely long service name
    # ---------------------------------------------------------

    def test_extremely_long_service_name_rejected(self):
        response = self.client.post(
            "/api/v1/services/",
            {
                "provider": self.provider.id,
                "name": "A" * 1000,
                "description": "Test service",
                "price": 500,
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 6. Invalid service price
    # ---------------------------------------------------------

    def test_invalid_service_price_rejected(self):
        response = self.client.post(
            "/api/v1/services/",
            {
                "provider": self.provider.id,
                "name": "Invalid Price Service",
                "description": "Test service",
                "price": "not-a-number",
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 7. Negative service price
    # ---------------------------------------------------------

    def test_negative_service_price_rejected(self):
        response = self.client.post(
            "/api/v1/services/",
            {
                "provider": self.provider.id,
                "name": "Negative Price Service",
                "description": "Test service",
                "price": -500,
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 8. Unexpected booking field
    # ---------------------------------------------------------

    def test_unexpected_booking_field_rejected(self):
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "service": self.service.id,
                "booking_date": "2026-10-01T10:00:00Z",
                "notes": "Test booking",
                "unexpected_field": "malicious-value",
            },
            format="json",
        )

        assert response.status_code == 400

    # ---------------------------------------------------------
    # 9. Unexpected service field
    # ---------------------------------------------------------

    def test_unexpected_service_field_rejected(self):
        response = self.client.post(
            "/api/v1/services/",
            {
                "provider": self.provider.id,
                "name": "Test Service",
                "description": "Test service",
                "price": 500,
                "unexpected_field": "malicious-value",
            },
            format="json",
        )

        assert response.status_code == 400