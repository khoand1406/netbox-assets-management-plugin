"""
API serializers for NetBox assets-management Plugin.

Serializers are required for NetBox event handling (webhooks, change logging).
They also power the REST API endpoints.

For more information on NetBox REST API serializers, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#serializers

For Django REST Framework serializers, see:
https://www.django-rest-framework.org/api-guide/serializers/
"""

from netbox.api.serializers import NetBoxModelSerializer

from ..models import Asset, AssetGroup



class AssetGroupSerializer(NetBoxModelSerializer):
    class Meta:
        model = AssetGroup
        fields= "__all__"
        
class AssetSerializer(NetBoxModelSerializer):
    class Meta:
        model = Asset
        fields= "__all__"
