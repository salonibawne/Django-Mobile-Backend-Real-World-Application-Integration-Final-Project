from django.urls import path

from .views import (
    ProviderCreateView,
    ProviderProfileView,
)


urlpatterns = [

    path(
        "",
        ProviderCreateView.as_view(),
        name="provider-create",
    ),

    path(
        "profile/",
        ProviderProfileView.as_view(),
        name="provider-profile",
    ),
]