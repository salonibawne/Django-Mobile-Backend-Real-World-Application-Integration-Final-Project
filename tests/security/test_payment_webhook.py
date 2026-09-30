import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.payments.models import Payment
from apps.providers.models import Provider
from apps.services.models import Service


@pytest.mark.django_db
class TestPaymentWebhookAudit:

    def setup_method(self):
        self.client = APIClient()

        self.customer = User.objects.create_user(
            username="webhook@example.com",
            email="webhook@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

        provider_user = User.objects.create_user(
            username="webhookprovider@example.com",
            email="webhookprovider@example.com",
            password="TestPassword123!",
            role="PROVIDER",
        )

        provider = Provider.objects.create(
            user=provider_user,
            business_name="Webhook Provider",
            phone="9876543210",
            address="Test Address",
            city="Nagpur",
        )

        service = Service.objects.create(
            provider=provider,
            name="Webhook Service",
            description="Webhook security test service",
            price=500,
        )

        booking = Booking.objects.create(
            customer=self.customer,
            service=service,
            booking_date="2026-12-01T10:00:00Z",
            status="PENDING",
        )

        self.payment = Payment.objects.create(
            booking=booking,
            amount=500,
            transaction_id="INITIAL-TRANSACTION",
            payment_status=Payment.Status.PENDING,
            payment_method=Payment.Method.MOCK,
        )

    def test_unauthenticated_webhook_cannot_change_payment_status(self):
        response = self.client.post(
            "/api/v1/payments/webhook/",
            {
                "event": "payment.success",
                "payment_id": self.payment.id,
                "transaction_id": "ATTACKER-TRANSACTION",
            },
            format="json",
        )

        assert response.status_code == 401

        self.payment.refresh_from_db()

        assert self.payment.payment_status == Payment.Status.PENDING
        assert self.payment.transaction_id == "INITIAL-TRANSACTION"