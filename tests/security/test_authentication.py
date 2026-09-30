import pytest
from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


@pytest.mark.django_db
class TestAuthenticationAudit:

    def setup_method(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="customer@example.com",
            email="customer@example.com",
            password="TestPassword123!",
            role="CUSTOMER",
        )

    def test_missing_token_rejected(self):
        response = self.client.get(
            "/api/v1/bookings/"
        )

        assert response.status_code == 401

    def test_invalid_token_rejected(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        response = self.client.get(
            "/api/v1/bookings/"
        )

        assert response.status_code == 401

    def test_login_returns_access_and_refresh_tokens(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {
                "username": "customer@example.com",
                "password": "TestPassword123!",
            },
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_refresh_token_works(self):
        refresh = RefreshToken.for_user(self.user)

        response = self.client.post(
            "/api/v1/auth/refresh/",
            {
                "refresh": str(refresh),
            },
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data

    def test_expired_access_token_rejected(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token

        access.set_exp(
            from_time=timezone.now() - timedelta(minutes=5)
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(access)}"
        )

        response = self.client.get(
            "/api/v1/bookings/"
        )

        assert response.status_code == 401

    def test_logout_blacklists_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/auth/logout/",
            {
                "refresh": str(refresh),
            },
            format="json",
        )

        assert response.status_code == 200

        response = self.client.post(
            "/api/v1/auth/refresh/",
            {
                "refresh": str(refresh),
            },
            format="json",
        )

        assert response.status_code == 401

    def test_password_change(self):
        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.post(
            "/api/v1/auth/password-change/",
            {
                "old_password": "TestPassword123!",
                "new_password": "NewTestPassword456!",
            },
            format="json",
        )

        assert response.status_code == 200

        self.user.refresh_from_db()

        assert self.user.check_password(
            "NewTestPassword456!"
        )