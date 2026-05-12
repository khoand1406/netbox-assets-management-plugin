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

from .models import Asset, AssetGroup, Assetsmanagement



        
class AssetGroupTable(NetBoxTable):
    """
    Bảng hiển thị danh sách nhóm tài sản
    """
    name = tables.Column(
        linkify=True,
        verbose_name='Name'
    )
    code = tables.Column(
        verbose_name='Code'
    )
    status = columns.ChoiceFieldColumn(
        verbose_name='Status'
    )
    description = tables.Column(
        verbose_name='Description',
        orderable=False
    )
    created = columns.DateTimeColumn(
        verbose_name='Created'
    )
    created_by = tables.Column(
        verbose_name='Created By'
    )
    last_updated = columns.DateTimeColumn(
        verbose_name='Last Updated'
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
        verbose_name="Name"
    )

    # Mã
    code = tables.Column(
        verbose_name="Code"
    )

    
    status = columns.ChoiceFieldColumn(
        verbose_name="Status"
    )

    
    site = tables.Column(
        linkify=True,
        verbose_name="Site"
    )

    
    location = tables.Column(
        linkify=True,
        verbose_name="Location"
    )

   
    asset_group = tables.Column(
        linkify=True,
        verbose_name="Asset Group"
    )

    
    manufacturer = tables.Column(
        verbose_name="Manufacturer"
    )

    
    device_type = tables.Column(
        verbose_name="Device Type"
    )

    created_by = tables.Column(
        linkify=True,
        verbose_name="Created By"
    )

    
    created = columns.DateTimeColumn(
        verbose_name="Created"
    )

    
    last_updated = columns.DateTimeColumn(
        verbose_name="Last Updated"
    )

    class Meta(NetBoxTable.Meta):
        model = Asset

        # Các cột mặc định hiển thị
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

        # Các cột hiển thị mặc định khi mở màn hình
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

        # Sắp xếp mặc định: cập nhật mới nhất lên đầu tiên
        order_by = ("-last_updated",)