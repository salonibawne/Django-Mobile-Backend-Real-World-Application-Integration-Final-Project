import uuid


class MockPaymentGateway:

    @staticmethod
    def process_payment(payment):
        """
        Simulate a payment gateway.

        No card information is accepted or stored.
        The mock gateway generates a transaction ID
        and returns a payment result.
        """

        transaction_id = f"MOCK-{uuid.uuid4().hex[:12].upper()}"

        # For now, simulate a successful gateway response.
        return {
            "event": "payment.success",
            "transaction_id": transaction_id,
            "amount": str(payment.amount),
            "payment_id": payment.id,
        }