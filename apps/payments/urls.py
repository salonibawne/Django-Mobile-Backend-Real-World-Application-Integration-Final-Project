from django.urls import path

from .views import (
    PaymentDetailView,
    PaymentInitiateView,
    PaymentListView,
    PaymentWebhookView,
)

urlpatterns = [
    path(
        "initiate/",
        PaymentInitiateView.as_view(),
        name="payment-initiate",
    ),
    path(
        "",
        PaymentListView.as_view(),
        name="payment-list",
    ),
    path(
        "<int:pk>/",
        PaymentDetailView.as_view(),
        name="payment-detail",
    ),
    
    path(
    "webhook/",
    PaymentWebhookView.as_view(),
    name="payment-webhook",
    ),
]

    