"""
Filtersets for NetBox assets-management Plugin.

For more information on NetBox filtersets, see:
https://docs.netbox.dev/en/stable/plugins/development/filtersets/

For django-filters documentation, see:
https://django-filter.readthedocs.io/
"""

import django_filters
from django.db.models import Q
from extras.filters import TagFilter
from dcim.models.sites import Location
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filtersets import register_filterset

from .models import Asset, AssetGroup, Assetsmanagement


@register_filterset
class AssetGroupFilterSet(NetBoxModelFilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Tên"
    )

    status = django_filters.MultipleChoiceFilter(
        choices=AssetGroup._meta.get_field("status").choices,
        label="Trạng thái"
    )

    tag= TagFilter()
    

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
    # Free-text search
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Tên",
    )

    location = django_filters.ModelChoiceFilter(
        queryset=Location.objects.all(),
        label="Vị trí",
    )

    
    asset_group = django_filters.ModelChoiceFilter(
        queryset=AssetGroup.objects.all(),
        label="Nhóm tài sản",
    )

   
    asset_group_id = django_filters.ModelChoiceFilter(
        field_name="asset_group",
        queryset=AssetGroup.objects.all(),
        to_field_name="id",
        label="Nhóm tài sản",
    )

    manufacturer = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Hãng sản xuất",
    )

    device_type = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Loại thiết bị",
    )
    tag= TagFilter()

    class Meta:
        model = Asset
        fields = (
            "q",
            "name",
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