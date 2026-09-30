from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            "id",
            "customer",
            "service",
            "booking_date",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "customer",
            "status",
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