from decimal import Decimal

from rest_framework import serializers

from .models import Service, ServiceImage


class ServiceSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.00")
    )

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

    def validate(self, attrs):
        allowed_fields = set(self.fields.keys())
        submitted_fields = set(self.initial_data.keys())

        unexpected_fields = submitted_fields - allowed_fields

        if unexpected_fields:
            raise serializers.ValidationError({
                "unexpected_fields": (
                    f"Unexpected fields: {', '.join(sorted(unexpected_fields))}"
                )
            })

        return attrs


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