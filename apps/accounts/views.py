from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import success_response

from .models import Profile, User
from .serializers import (
    ProfileImageSerializer,
    ProfileSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

        profile, _created = Profile.objects.get_or_create(
            user=self.request.user
        )

        return profile


class ProfileImageUploadView(generics.GenericAPIView):

    serializer_class = ProfileImageSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_object(self):

        profile, _created = Profile.objects.get_or_create(
            user=self.request.user
        )

        return profile

    def post(self, request):

        profile = self.get_object()

        serializer = self.get_serializer(
            profile,
            data=request.data,
            partial=False
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return success_response(
    message="Profile image uploaded successfully.",
    data=serializer.data,
    status_code=status.HTTP_200_OK,
)