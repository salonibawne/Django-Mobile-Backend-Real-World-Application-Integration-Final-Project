import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.accounts.models import Profile
from apps.bookings.models import Booking
from apps.services.models import Service
from apps.providers.models import Provider


@pytest.mark.django_db
class TestIDORAudit:

    def setup_method(self):
        self.client = APIClient()

        # Customer A
        self.customer_a = User.objects.create_user(
            username="customer_a@example.com",
            email="customer_a@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

        # Customer B
        self.customer_b = User.objects.create_user(
            username="customer_b@example.com",
            email="customer_b@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

        # Provider A
        self.provider_a_user = User.objects.create_user(
            username="provider_a@example.com",
            email="provider_a@example.com",
            password="TestPassword123!",
            role="PROVIDER",
        )

        # Provider B
        self.provider_b_user = User.objects.create_user(
            username="provider_b@example.com",
            email="provider_b@example.com",
            password="TestPassword123!",
            role="PROVIDER",
        )

        # Provider A profile
        self.provider_a = Provider.objects.create(
            user=self.provider_a_user,
            business_name="Provider A",
            phone="9876543210",
            address="Address A",
            city="Nagpur",
        )

        # Provider B profile
        self.provider_b = Provider.objects.create(
            user=self.provider_b_user,
            business_name="Provider B",
            phone="9876543211",
            address="Address B",
            city="Nagpur",
        )

        # Services
        self.service_a = Service.objects.create(
            provider=self.provider_a,
            name="Service A",
            description="Service provided by Provider A",
            price=500,
        )

        self.service_b = Service.objects.create(
            provider=self.provider_b,
            name="Service B",
            description="Service provided by Provider B",
            price=600,
        )

        # Profiles
        self.profile_a, _ = Profile.objects.get_or_create(
            user=self.customer_a
        )

        self.profile_b, _ = Profile.objects.get_or_create(
            user=self.customer_b
        )

        # Customer B booking
        self.booking_b = Booking.objects.create(
            customer=self.customer_b,
            service=self.service_b,
            booking_date="2026-10-01T10:00:00Z",
            status="PENDING",
        )

    # ---------------------------------------------------------
    # Customer A -> Customer B Profile
    # ---------------------------------------------------------

    def test_customer_cannot_access_other_customer_profile(self):
        self.client.force_authenticate(
            user=self.customer_a
        )

        response = self.client.get(
            "/api/v1/auth/profile/"
        )

        # Profile endpoint should return only the logged-in
        # customer's profile.
        assert response.status_code == 200

        data = response.json()

        assert data.get("id") != self.profile_b.id

    # ---------------------------------------------------------
    # Customer A -> Customer B Booking
    # ---------------------------------------------------------

    def test_customer_cannot_access_other_customer_booking(self):
        self.client.force_authenticate(
            user=self.customer_a
        )

        response = self.client.get(
            f"/api/v1/bookings/{self.booking_b.id}/"
        )

        assert response.status_code in [403, 404]

    # ---------------------------------------------------------
    # Provider A -> Provider B Service Image
    # ---------------------------------------------------------

    def test_provider_cannot_modify_other_provider_service(self):
        self.client.force_authenticate(
            user=self.provider_a_user
        )

        response = self.client.post(
            f"/api/v1/services/{self.service_b.id}/images/",
            {},
            format="multipart",
        )

        assert response.status_code in [403, 404]