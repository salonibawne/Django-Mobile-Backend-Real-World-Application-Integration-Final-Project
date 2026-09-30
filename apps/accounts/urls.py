from django.urls import path

from .views import (
    LogoutView,
    PasswordChangeView,
    ProfileImageUploadView,
    ProfileView,
    RegisterView,
)


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "profile/image/",
        ProfileImageUploadView.as_view(),
        name="profile-image-upload",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "password-change/",
        PasswordChangeView.as_view(),
        name="password-change",
    ),
]