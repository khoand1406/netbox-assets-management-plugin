"""
Tables for NetBox assets-management Plugin.

For more information on NetBox tables, see:
https://docs.netbox.dev/en/stable/plugins/development/tables/

For django-tables2 documentation, see:
https://django-tables2.readthedocs.io/
"""

import django_tables2 as tables
from netbox.tables import NetBoxTable
from netbox.tables import columns

from .models import Asset, AssetGroup
from django.utils.translation import gettext_lazy as _


class AssetGroupTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        verbose_name=_('Name')
    )
    code = tables.Column(
        verbose_name=_('Code')
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_('Status')
    )
    description = tables.Column(
        verbose_name=_('Description'),
        orderable=False
    )
    created = columns.DateTimeColumn(
        verbose_name=_('Created')
    )
    created_by = tables.Column(
        verbose_name=_('Created By')
    )
    last_updated = columns.DateTimeColumn(
        verbose_name=_('Last Updated')
    )

    class Meta(NetBoxTable.Meta):
        model = AssetGroup
        fields = (
            'pk', 'name', 'code', 'status', 'description',
            'created', 'created_by', 'last_updated', 'actions'
        )
        default_columns = (
            'name', 'code', 'status', 'description',
            'created', 'created_by', 'last_updated', 'actions'
        )


class AssetTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
        verbose_name=_("Name")
    )
    code = tables.Column(
        verbose_name=_("Code")
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_("Status")
    )
    site = tables.Column(
        linkify=True,
        verbose_name=_("Site")
    )
    location = tables.Column(
        linkify=True,
        verbose_name=_("Location")
    )
    asset_group = tables.Column(
        linkify=True,
        verbose_name=_("Asset Group")
    )
    manufacturer = tables.Column(
        verbose_name=_("Manufacturer")
    )
    device_type = tables.Column(
        verbose_name=_("Device Type")
    )
    created_by = tables.Column(
        linkify=True,
        verbose_name=_("Created By")
    )
    created = columns.DateTimeColumn(
        verbose_name=_("Created")
    )
    last_updated = columns.DateTimeColumn(
        verbose_name=_("Last Updated")
    )

    class Meta(NetBoxTable.Meta):
        model = Asset
        fields = (
            "pk",
            "id",
            "name",
            "code",
            "status",
            "site",
            "location",
            "asset_group",
            "manufacturer",
            "device_type",
            "created_by",
            "created",
            "last_updated",
            "actions",
        )
        default_columns = (
            "name",
            "code",
            "status",
            "site",
            "location",
            "asset_group",
            "manufacturer",
            "device_type",
            "created_by",
            "created",
            "last_updated",
            "actions",
        )
        order_by = ("-last_updated",)