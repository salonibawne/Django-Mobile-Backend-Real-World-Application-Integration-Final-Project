from django.urls import path

from .views import (
    RegisterView,
    ProfileView,
    ProfileImageUploadView,
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