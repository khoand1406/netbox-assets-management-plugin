

from django import forms
from dcim.models.sites import Location, Region, Site
from extras.models.tags import Tag
from netbox.forms.bulk_import import PrimaryModelImportForm
from utilities.forms.fields.csv import CSVChoiceField
from utilities.forms.fields.csv import CSVModelMultipleChoiceField
from utilities.forms.fields.csv import CSVModelChoiceField
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .choices import AssetStatusChoices, AssetsManagemnentChoice
from .models import AssetGroup, Asset

class AssetGroupCSVForm(PrimaryModelImportForm):
    status = CSVChoiceField(
        choices=AssetsManagemnentChoice,
        required=False,
        label="Status"
    )

    excluded_from_visualization = forms.BooleanField(
        required=False,
        label="Exclude from Visualization",
        help_text=(
            "Accepted values: true/false, yes/no, 1/0."
        ),
    )
    tags = CSVModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(AssetGroup)
        ) | Tag.objects.filter(object_types__isnull=True),  # tag không giới hạn model nào thì vẫn dùng được
        to_field_name="name",
        required=False,
        label="Tags",
        help_text=_("Comma-separated list of tag names"),
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
    status = CSVChoiceField(
        choices=AssetStatusChoices,
        required=False,
        initial=AssetStatusChoices.ACTIVE,
        label="Status"
    )
    
    tags = CSVModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(Asset)
        ) | Tag.objects.filter(object_types__isnull=True),  # tag không giới hạn model nào thì vẫn dùng được
        to_field_name="name",
        required=False,
        label="Tags",
        help_text=_("Comma-separated list of tag names"),
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
            "tags",
            "region",
            "site",
            "location",
            "installation_date",
            "purchase_date",
            "warranty_period_months",
            
        )

