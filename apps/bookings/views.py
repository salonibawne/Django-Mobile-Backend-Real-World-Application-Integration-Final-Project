from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking
from .serializers import BookingSerializer


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            customer=request.user
        ).order_by("-created_at")

        serializer = BookingSerializer(bookings, many=True)

        return Response({
            "success": True,
            "message": "Bookings retrieved successfully",
            "data": serializer.data,
        })

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(customer=request.user)

            return Response(
                {
                    "success": True,
                    "message": "Booking created successfully",
                    "data": BookingSerializer(booking).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "message": "Booking creation failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            booking = Booking.objects.get(
                pk=pk,
                customer=request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Booking not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BookingSerializer(booking)

        return Response({
            "success": True,
            "message": "Booking retrieved successfully",
            "data": serializer.data,
        })


class BookingConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Booking not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        booking.status = "CONFIRMED"
        booking.save(update_fields=["status"])

        serializer = BookingSerializer(booking)

        return Response({
            "success": True,
            "message": "Booking confirmed successfully",
            "data": serializer.data,
        })


class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(
                pk=pk,
                customer=request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Booking not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        booking.status = "CANCELLED"
        booking.save(update_fields=["status"])

        serializer = BookingSerializer(booking)

        return Response({
            "success": True,
            "message": "Booking cancelled successfully",
            "data": serializer.data,
        })


class BookingCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Booking not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        booking.status = "COMPLETED"
        booking.save(update_fields=["status"])

        serializer = BookingSerializer(booking)

        return Response({
            "success": True,
            "message": "Booking completed successfully",
            "data": serializer.data,
        })