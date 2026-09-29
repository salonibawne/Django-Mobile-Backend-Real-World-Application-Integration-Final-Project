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