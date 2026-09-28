from rest_framework import serializers

from .models import Provider


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider

        fields = [
            "id",
            "user",
            "business_name",
            "phone",
            "address",
            "city",
            "is_verified",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "is_verified",
            "created_at",
        ]