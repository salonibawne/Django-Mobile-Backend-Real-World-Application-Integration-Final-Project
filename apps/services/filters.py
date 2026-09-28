import django_filters

from .models import Service


class ServiceFilter(django_filters.FilterSet):

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte"
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte"
    )

    provider = django_filters.NumberFilter(
        field_name="provider_id"
    )

    is_available = django_filters.BooleanFilter(
        field_name="is_available"
    )

    class Meta:
        model = Service
        fields = [
            "provider",
            "is_available",
            "min_price",
            "max_price",
        ]