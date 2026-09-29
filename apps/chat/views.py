from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import error_response, success_response

from .models import Message
from .serializers import MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            booking__customer=self.request.user
        ).order_by("created_at") | Message.objects.filter(
            booking__service__provider__user=self.request.user
        ).order_by("created_at")

    def perform_create(self, serializer):
        booking = serializer.validated_data["booking"]

        # User must be either the customer or the service provider
        if (
            booking.customer != self.request.user
            and booking.service.provider.user != self.request.user
        ):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You can only send messages for your own bookings."
            )

        serializer.save(sender=self.request.user)


class MessageDetailView(generics.RetrieveAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db.models import Q

        return Message.objects.filter(
            Q(booking__customer=self.request.user)
            | Q(booking__service__provider__user=self.request.user)
        )

class MessageMarkReadView(generics.GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        from django.db.models import Q

        message = Message.objects.filter(
            Q(booking__customer=request.user)
            | Q(booking__service__provider__user=request.user),
            pk=pk
        ).first()

        if not message:
            return error_response(
                message="Message not found.",
                error_code="MESSAGE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        message.is_read = True
        message.save(update_fields=["is_read"])

        return success_response(
            message="Message marked as read successfully.",
            data=MessageSerializer(message).data,
            status_code=status.HTTP_200_OK,
        )