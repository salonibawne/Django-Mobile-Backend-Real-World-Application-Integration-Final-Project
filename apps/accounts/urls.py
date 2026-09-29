from django.urls import path

from .views import (
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
]