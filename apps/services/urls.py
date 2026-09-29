from django.urls import path

from .views import (
    ServiceImageDeleteView,
    ServiceImageListCreateView,
    ServiceListCreateView,
)

urlpatterns = [
    path(
        "",
        ServiceListCreateView.as_view(),
        name="service-list-create",
    ),

    path(
        "<int:service_id>/images/",
        ServiceImageListCreateView.as_view(),
        name="service-images",
    ),

    path(
        "<int:service_id>/images/<int:pk>/",
        ServiceImageDeleteView.as_view(),
        name="service-image-delete",
    ),
]