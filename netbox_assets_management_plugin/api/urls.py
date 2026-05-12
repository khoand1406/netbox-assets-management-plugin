"""
API URL patterns for NetBox assets-management Plugin.

For more information on NetBox REST API routing, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#routers

For Django REST Framework routers, see:
https://www.django-rest-framework.org/api-guide/routers/
"""

from netbox.api.routers import NetBoxRouter

from .views import AssetGroupViewSet, AssetViewSet

app_name = "netbox_assets_management_plugin"

router = NetBoxRouter()
router.register(
    "asset-groups",
    AssetGroupViewSet,
    basename="assetgroup"
)

router.register(
    "assets",
    AssetViewSet,
    basename="asset"
)

urlpatterns = router.urls

