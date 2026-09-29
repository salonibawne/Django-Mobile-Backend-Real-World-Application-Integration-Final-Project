from django.urls import path

from .views import (
    BookingCancelView,
    BookingCompleteView,
    BookingConfirmView,
    BookingDetailView,
    BookingListCreateView,
)

urlpatterns = [
    path("", BookingListCreateView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),
    path("<int:pk>/confirm/", BookingConfirmView.as_view(), name="booking-confirm"),
    path("<int:pk>/complete/", BookingCompleteView.as_view(), name="booking-complete"),
]