import io

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.providers.models import Provider
from apps.services.models import Service, ServiceImage


@pytest.mark.django_db
class TestFileUploadAudit:

    def setup_method(self):
        self.client = APIClient()

        self.provider_user = User.objects.create_user(
            username="provider@example.com",
            email="provider@example.com",
            password="TestPassword123!",
            role="PROVIDER",
        )

        self.other_provider_user = User.objects.create_user(
            username="otherprovider@example.com",
            email="otherprovider@example.com",
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

        self.other_provider = Provider.objects.create(
            user=self.other_provider_user,
            business_name="Other Provider",
            phone="9876543211",
            address="Other Address",
            city="Nagpur",
        )

        self.service = Service.objects.create(
            provider=self.provider,
            name="Test Service",
            description="Test service for file upload security",
            price=500,
        )

        self.other_service = Service.objects.create(
            provider=self.other_provider,
            name="Other Service",
            description="Other provider service",
            price=600,
        )

    def create_valid_image(self, filename="test.jpg"):
        image = Image.new("RGB", (100, 100), "white")

        image_file = io.BytesIO()
        image.save(image_file, format="JPEG")
        image_file.seek(0)

        return SimpleUploadedFile(
            filename,
            image_file.read(),
            content_type="image/jpeg",
        )

    def test_missing_file_is_rejected(self):
        self.client.force_authenticate(user=self.provider_user)

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {},
            format="multipart",
        )

        assert response.status_code == 400

    def test_invalid_extension_is_rejected(self):
        self.client.force_authenticate(user=self.provider_user)

        malicious_file = SimpleUploadedFile(
            "malware.exe",
            b"MZ fake executable content",
            content_type="application/octet-stream",
        )

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {"image": malicious_file},
            format="multipart",
        )

        assert response.status_code == 400

    def test_large_file_is_rejected(self):
        self.client.force_authenticate(user=self.provider_user)

        large_file = SimpleUploadedFile(
            "large.jpg",
            b"x" * (6 * 1024 * 1024),
            content_type="image/jpeg",
        )

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {"image": large_file},
            format="multipart",
        )

        assert response.status_code == 400

    def test_malicious_filename_is_rejected(self):
        self.client.force_authenticate(user=self.provider_user)

        malicious_file = SimpleUploadedFile(
            "../../malicious.php",
            b"<?php echo 'malicious'; ?>",
            content_type="image/jpeg",
        )

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {"image": malicious_file},
            format="multipart",
        )

        assert response.status_code == 400

    def test_incorrect_mime_type_is_rejected(self):
        self.client.force_authenticate(user=self.provider_user)

        fake_image = SimpleUploadedFile(
            "fake.jpg",
            b"This is not actually an image",
            content_type="image/jpeg",
        )

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {"image": fake_image},
            format="multipart",
        )

        assert response.status_code == 400

    def test_valid_image_is_accepted(self):
        self.client.force_authenticate(user=self.provider_user)

        image_file = self.create_valid_image()

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {"image": image_file},
            format="multipart",
        )

        assert response.status_code == 201
        assert ServiceImage.objects.filter(
            service=self.service
        ).exists()

    def test_other_provider_cannot_upload_to_service(self):
        self.client.force_authenticate(user=self.other_provider_user)

        image_file = self.create_valid_image("other.jpg")

        response = self.client.post(
            f"/api/v1/services/{self.service.id}/images/",
            {"image": image_file},
            format="multipart",
        )

        assert response.status_code == 403