from rest_framework import serializers

from .models import Service, ServiceImage


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service

        fields = [
            "id",
            "provider",
            "name",
            "description",
            "price",
            "is_available",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ServiceImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceImage

        fields = [
            "id",
            "service",
            "image",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "service",
            "created_at",
        ]