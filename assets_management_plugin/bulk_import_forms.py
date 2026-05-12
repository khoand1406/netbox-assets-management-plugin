

from django import forms
from dcim.models.sites import Location, Region, Site
from netbox.forms.bulk_import import PrimaryModelImportForm
from utilities.forms.fields.csv import CSVModelChoiceField
from .choices import AssetStatusChoices, AssetsManagemnentChoice
from .models import AssetGroup, Asset

class AssetGroupCSVForm(PrimaryModelImportForm):
    status = forms.ChoiceField(
        choices=AssetsManagemnentChoice,
        required=False,
        initial=AssetsManagemnentChoice.STATUS_ACTIVE,
        label="Status"
    )

    excluded_from_visualization = forms.BooleanField(
        required=False,
        label="Exclude from Visualization",
        help_text=(
            "Accepted values: true/false, yes/no, 1/0."
        ),
    )

    class Meta:
        model = AssetGroup
        fields = (
            "name",
            "code",
            "status",
            "description",
            "excluded_from_visualization",
        )
    def save(self, *args, **kwargs):
        
        obj = self.instance

        if obj.pk is None and not obj.created_by and hasattr(self, "request"):
            obj.created_by = self.request.user

        return super().save(*args, **kwargs)

class AssetCSVForm(PrimaryModelImportForm):
    model= Asset
    asset_group= CSVModelChoiceField(
        queryset=AssetGroup.objects.all(),
        to_field_name="name",
        required=False,
        help_text="Enter Asset group name"
        
    )
    region = CSVModelChoiceField(
        queryset=Region.objects.all(),
        to_field_name="name",
        required=False,
        label="Region"
    )

    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        to_field_name="name",
        required=False,
        label="Site"
    )

    location = CSVModelChoiceField(
        queryset=Location.objects.all(),
        to_field_name="name",
        required=False,
        label="Location"
    )

    # Choice field
    status = forms.ChoiceField(
        choices=AssetStatusChoices,
        required=False,
        initial=AssetStatusChoices.ACTIVE,
        label="Status"
    )
    class Meta:
        model = Asset
        fields = (
            "name",
            "code",
            "asset_group",
            "status",
            "description",
            "device_type",
            "model",
            "serial",
            "manufacturer",
            "region",
            "site",
            "location",
            "installation_date",
            "purchase_date",
            "warranty_period_months",
            
        )

