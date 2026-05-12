"""
URL patterns for NetBox assets-management Plugin.

For more information on URL routing, see:
https://docs.netbox.dev/en/stable/plugins/development/views/#url-registration

For Django URL patterns, see:
https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views



urlpatterns = (
    path(
        "assets-managements/",
        views.AssetGroupListView.as_view(),
        name="assetgroup_list"
    ),
    path(
        "assets-managements/add/",
        views.AssetGroupCreateView.as_view(),
        name="assetgroup_add"
    ),
    path(
        "assets-managements/<int:pk>/",
        views.AssetGroupView.as_view(),
        name="assetgroup"
    ),
    path(
        "assets-managements/<int:pk>/edit/",
        views.AssetGroupEditView.as_view(),
        name="assetgroup_edit"
    ),
    path(
        "assets-managements/<int:pk>/delete/",
        views.AssetGroupDeleteView.as_view(),
        name="assetgroup_delete"
    ),
    path("assets-managements/edit/", views.AssetGroupBulkEditView.as_view(), name="assetgroup_bulk_edit"),
    path("assets-managements/delete/", views.AssetGroupBulkDeleteView.as_view(), name="assetgroup_bulk_delete"),
    path("assets-managements/import/", views.AssetGroupBulkImportView.as_view(), name="assetgroup_bulk_import"),
    path(
        "assets-managements/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="assetgroup_changelog",
        kwargs={"model": models.AssetGroup},
    ),
    
    path(
        "assets-managements/assets/",
        views.AssetListView.as_view(),
        name="asset_list"
    ),
    path(
        "assets-managements/assets/<int:pk>/",
        views.AssetView.as_view(),
        name="asset",
    ),
    path(
        "assets-managements/assets/add/",
        views.AssetCreateView.as_view(),
        name="asset_add"
    ),
    path(
        "assets-managements/assets/<int:pk>/edit/",
        views.AssetEditView.as_view(),
        name="asset_edit"
    ),
    path(
        "assets-managements/assets/import",
        views.AssetBulkImportView.as_view(),
        name="asset_bulk_import"
    ),
    path(
        "assets-managements/assets/<int:pk>/delete/",
        views.AssetDeleteView.as_view(),
        name="asset_delete"
    ),
    path("assets-managements/assets/edit/", views.AssetBulkEditView.as_view(), name="asset_bulk_edit"),
    path("assets-managements/assets/delete/", views.AssetBulkDeleteView.as_view(), name="asset_bulk_delete"),
    path(
        "assets-managements/assets/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="asset_changelog",
        kwargs={"model": models.Asset},
    ),
    
)