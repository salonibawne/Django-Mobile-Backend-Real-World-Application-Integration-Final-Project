from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import error_response, success_response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return success_response(
            message="Notifications retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    def retrieve(self, request, *args, **kwargs):
        notification = self.get_object()

        return success_response(
            message="Notification retrieved successfully.",
            data=self.get_serializer(notification).data,
            status_code=status.HTTP_200_OK,
        )


class NotificationMarkReadView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.filter(
            pk=pk,
            user=request.user
        ).first()

        if not notification:
            return error_response(
                message="Notification not found.",
                error_code="NOTIFICATION_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        notification.is_read = True
        notification.save()

        return success_response(
            message="Notification marked as read successfully.",
            data=NotificationSerializer(notification).data,
            status_code=status.HTTP_200_OK,
        )