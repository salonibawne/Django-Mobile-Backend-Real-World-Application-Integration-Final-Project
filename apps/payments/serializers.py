from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "booking",
            "amount",
            "transaction_id",
            "payment_status",
            "payment_method",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "amount",
            "transaction_id",
            "payment_status",
            "payment_method",
            "created_at",
        ]