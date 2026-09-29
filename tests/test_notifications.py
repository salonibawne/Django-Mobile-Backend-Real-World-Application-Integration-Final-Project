import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.notifications.models import Notification


@pytest.mark.django_db
def test_notification_list():
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username="notification@example.com",
        email="notification@example.com",
        password="Test@123",
    )

    Notification.objects.create(
        user=user,
        notification_type="BOOKING_CREATED",
        title="Booking Created",
        message="Your booking has been created.",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/v1/notifications/")

    assert response.status_code == 200