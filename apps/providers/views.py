from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import success_response, error_response

from .models import Provider
from .serializers import ProviderSerializer


class ProviderCreateView(generics.CreateAPIView):

    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        if hasattr(request.user, "provider_profile"):
            return error_response(
                message="Provider profile already exists.",
                error_code="PROVIDER_ALREADY_EXISTS",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.save(user=request.user)

        return success_response(
            message="Provider profile created successfully.",
            data=ProviderSerializer(provider).data,
            status_code=status.HTTP_201_CREATED,
        )


class ProviderProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        try:
            return Provider.objects.get(user=self.request.user)

        except Provider.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):

        provider = self.get_object()

        if not provider:
            return error_response(
                message="Provider profile not found.",
                error_code="PROVIDER_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return success_response(
            message="Provider profile retrieved successfully.",
            data=self.get_serializer(provider).data,
            status_code=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):

        provider = self.get_object()

        if not provider:
            return error_response(
                message="Provider profile not found.",
                error_code="PROVIDER_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(
            provider,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return success_response(
            message="Provider profile updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )