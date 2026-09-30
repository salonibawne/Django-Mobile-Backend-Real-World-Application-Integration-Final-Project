from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.common.responses import success_response

from .models import Profile, User
from .serializers import (
    PasswordChangeSerializer,
    ProfileImageSerializer,
    ProfileSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):

        profile, _created = Profile.objects.get_or_create(
            user=self.request.user
        )

        return profile


class ProfileImageUploadView(generics.GenericAPIView):

    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]

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

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return success_response(
            message="Profile image uploaded successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class LogoutView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired refresh token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return success_response(
            message="Logout successful.",
            data=None,
            status_code=status.HTTP_200_OK,
        )


class PasswordChangeView(generics.GenericAPIView):

    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data,
            context={
                "request": request
            }
        )

        serializer.is_valid(raise_exception=True)

        request.user.set_password(
            serializer.validated_data["new_password"]
        )

        request.user.save(
            update_fields=["password"]
        )

        return success_response(
            message="Password changed successfully.",
            data=None,
            status_code=status.HTTP_200_OK,
        )