from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import error_response, success_response

from .filters import ServiceFilter
from .models import Service, ServiceImage
from .serializers import (
    ServiceImageSerializer,
    ServiceSerializer,
)


class ServiceListCreateView(generics.ListCreateAPIView):

    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ServiceFilter
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]
    def get_queryset(self):
        queryset = Service.objects.all()

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return success_response(
                message="Services retrieved successfully.",
                data={
                    "count": self.paginator.page.paginator.count,
                    "next": self.paginator.get_next_link(),
                    "previous": self.paginator.get_previous_link(),
                    "results": serializer.data,
                },
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)

        return success_response(
            message="Services retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

class ServiceImageListCreateView(generics.GenericAPIView):

    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticated]

    def get_service(self, service_id):
        try:
            return Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return None

    def get(self, request, service_id):

        service = self.get_service(service_id)

        if not service:
            return error_response(
                message="Service not found.",
                error_code="SERVICE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        images = ServiceImage.objects.filter(
            service=service
        )

        serializer = self.get_serializer(
            images,
            many=True
        )

        return success_response(
            message="Service images retrieved successfully.",
            data=serializer.data,
        )

    def post(self, request, service_id):

        service = self.get_service(service_id)

        if not service:
            return error_response(
                message="Service not found.",
                error_code="SERVICE_NOT_FOUND",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Check that the logged-in user owns this service
        if service.provider.user != request.user:
            return error_response(
                message="You can only upload images for your own service.",
                error_code="SERVICE_ACCESS_DENIED",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save(
            service=service
        )

        return success_response(
            message="Service image uploaded successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class ServiceImageDeleteView(generics.DestroyAPIView):

    serializer_class = ServiceImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceImage.objects.filter(
            service__provider__user=self.request.user
        )

    def destroy(self, request, *args, **kwargs):

        image = self.get_object()

        image.delete()

        return success_response(
            message="Service image deleted successfully.",
            data=None,
        )