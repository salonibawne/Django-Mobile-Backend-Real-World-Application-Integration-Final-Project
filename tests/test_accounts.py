import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login():
    
    user_model = get_user_model()

    user_model.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="Test@123",
    )

    client = APIClient()

    response = client.post(
        "/api/v1/auth/login/",
        {
            "username": "test@example.com",
            "password": "Test@123",
        },
        format="json",
    )

    assert response.status_code == 200