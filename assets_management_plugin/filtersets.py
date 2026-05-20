import django_filters
from django.db.models import Q
from extras.filters import TagFilter
from dcim.models.sites import Location
from dcim.models.sites import Region, Site
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset
from django.utils.translation import gettext_lazy as _
from .models import Asset, AssetGroup


@register_filterset
class AssetGroupFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Name")
    )

    status = django_filters.MultipleChoiceFilter(
        choices=AssetGroup._meta.get_field("status").choices,
        label=_("Status")
    )

    tag = TagFilter()

    class Meta:
        model = AssetGroup
        fields = ("q", "name", "status", "tag")

    def search(self, queryset, name, value):
        if not value or not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) |
            Q(code__icontains=value) |
            Q(description__icontains=value)
        )


@register_filterset
class AssetFilterSet(NetBoxModelFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label=_("Search"),
    )

    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Name"),
    )

    status = django_filters.MultipleChoiceFilter(
        choices=Asset._meta.get_field("status").choices,
        label=_("Status"),
    )

    region = django_filters.ModelChoiceFilter(
        queryset=Region.objects.all(),
        label=_("Region"),
        method="filter_region",
    )

    site = django_filters.ModelChoiceFilter(
        queryset=Site.objects.all(),
        label=_("Site"),
        field_name="site",
    )

    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all(),
        label=_("Location"),
        field_name="location",
    )

    asset_group = django_filters.ModelChoiceFilter(
        queryset=AssetGroup.objects.all(),
        label=_("Asset Group"),
        field_name="asset_group",
    )

    asset_group_id = django_filters.ModelChoiceFilter(
        field_name="asset_group",
        queryset=AssetGroup.objects.all(),
        to_field_name="id",
        label=_("Asset Group"),
    )

    manufacturer = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Manufacturer"),
    )

    device_type = django_filters.CharFilter(
        lookup_expr="icontains",
        label=_("Device Type"),
    )

    tag = TagFilter()

    class Meta:
        model = Asset
        fields = (
            "q",
            "name",
            "status",
            "region",
            "site",
            "location",
            "asset_group",
            "asset_group_id",
            "manufacturer",
            "device_type",
            "tag",
        )

    def search(self, queryset, name, value):
        if not value or not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value)
            | Q(code__icontains=value)
            | Q(description__icontains=value)
            | Q(manufacturer__icontains=value)
            | Q(device_type__icontains=value)
        )

    def filter_region(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(region=value) | Q(site__region=value)
            )
        return queryset