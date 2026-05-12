"""
API viewsets for NetBox assets-management Plugin.

For more information on NetBox REST API viewsets, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#viewsets

For Django REST Framework viewsets, see:
https://www.django-rest-framework.org/api-guide/viewsets/
"""

from netbox.api.viewsets import NetBoxModelViewSet

from ..models import Assetsmanagement
from .serializers import AssetGroupSerializer, AssetSerializer


class AssetGroupViewSet(NetBoxModelViewSet):
    queryset = Assetsmanagement.objects.all()
    serializer_class = AssetGroupSerializer
    
class AssetViewSet(NetBoxModelViewSet):
    queryset = Assetsmanagement.objects.all()
    serializer_class = AssetSerializer

