from netbox.forms.bulk_edit import NetBoxModelBulkEditForm
from .models import Asset, AssetGroup
from .choices import AssetStatusChoices, AssetsManagemnentChoice

from django import forms
class AssetBulkEditForm(NetBoxModelBulkEditForm):
    model= Asset
    pk = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        widget=forms.MultipleHiddenInput
    )
    status = forms.ChoiceField(
        choices=AssetStatusChoices,
        required=False  
    )

class AssetGroupBulkEditForm(NetBoxModelBulkEditForm):
    model = AssetGroup
    pk = forms.ModelMultipleChoiceField(
        queryset=AssetGroup.objects.all(),
        widget=forms.MultipleHiddenInput
    )

    status = forms.ChoiceField(
        choices=AssetsManagemnentChoice,
        required=False
    )