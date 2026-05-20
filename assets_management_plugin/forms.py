"""
Forms for NetBox assets-management Plugin.

For more information on NetBox forms, see:
https://docs.netbox.dev/en/stable/plugins/development/forms/
"""
from django import forms
from dcim.models.sites import Location
from dcim.models.sites import Region, Site
from extras.models.models import ImageAttachment
from extras.models.tags import Tag
from netbox.forms import NetBoxModelForm
from django.core.validators import FileExtensionValidator
from utilities.forms.fields.dynamic import DynamicModelMultipleChoiceField
from utilities.forms.fields.fields import TagFilterField
from utilities.forms.fields import DynamicModelChoiceField
from netbox.forms.filtersets import NetBoxModelFilterSetForm
from utilities.forms.rendering import FieldSet
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from .models import Asset, AssetGroup, Assetsmanagement
from .ui.widgets import CustomUploadWidget, MultipleFileField


class AssetsmanagementForm(NetBoxModelForm):
    class Meta:
        model = Assetsmanagement
        fields = ("name", "tags")
        
class AssetGroupForm(NetBoxModelForm):
    """
    Form thêm mới/chỉnh sửa Asset Group.
    """
    attachment= MultipleFileField(
        required= False,
        label= _("Attachment"),
        help_text=_("Only jpg, jpeg, png allowed. Maximum total size per file: 25MB."),
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png"])
        ],
        widget=CustomUploadWidget(
           attrs= {
               "multiple": True
           }
        )
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

    def clean_attachment(self):
        files = self.files.getlist("attachment")

        if not files:
            return []

        allowed_extensions = {"jpg", "jpeg", "png"}
        max_size = 25 * 1024 * 1024

        for file in files:
            
            if file.size > max_size:
                raise forms.ValidationError(
                    f"File '{file.name}' exceeds 25MB."
                )

            
            extension = file.name.rsplit(".", 1)[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    f"File '{file.name}' has unsupported extension."
                )

        return files
    
class AssetGroupEditForm(NetBoxModelForm):
    # Upload ảnh mới
    attachment= MultipleFileField(
        required= False,
        label= _("Attachment"),
        help_text=_("Only jpg, jpeg, png allowed. Maximum total size per file: 25MB."),
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png"])
        ],
        widget=CustomUploadWidget(
           attrs= {
               "multiple": True
           }
        )
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.filter(
            object_types=ContentType.objects.get_for_model(AssetGroup)
        ) | Tag.objects.filter(object_types__isnull=True),
        required=False,
        label="Tags",
    )

    class Meta:
        model = AssetGroup
        fields = (
            "name",
            "code",
            "status",
            "description",
            "tags",
            "excluded_from_visualization",
        )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.fields["tags"].initial = self.instance.tags.all()
    
    def clean_attachment(self):
        files = self.files.getlist("attachment")

        if not files:
            return []

        allowed_extensions = {"jpg", "jpeg", "png"}
        max_size = 25 * 1024 * 1024

        for file in files:
            
            if file.size > max_size:
                raise forms.ValidationError(
                    f"File '{file.name}' exceeds 25MB."
                )

            
            extension = file.name.rsplit(".", 1)[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    f"File '{file.name}' has unsupported extension."
                )

        return files
              
class AssetGroupFilterForm(NetBoxModelFilterSetForm):
    model = AssetGroup

    name = forms.CharField(
        required=False,
        label=_("Name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter group name")}
        )
    )

    status = forms.MultipleChoiceField(
        choices=AssetGroup._meta.get_field("status").choices,
        required=False,
        label=_("Status"),
    )

    tag = TagFilterField(model=AssetGroup)

    fieldsets = (
        FieldSet("q"),
        FieldSet("name", "status", "tag", name=_("Asset Group")),
    )


class AssetFilterForm(NetBoxModelFilterSetForm):
    model = Asset

    q = forms.CharField(
        required=False,
        label=_("Search"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search by name, code, description, manufacturer, or device type")
            }
        )
    )

    name = forms.CharField(
        required=False,
        label=_("Name"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter asset name")}
        )
    )

    status = forms.MultipleChoiceField(
        required=False,
        label=_("Status"),
        choices=Asset._meta.get_field("status").choices,
    )

    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region"),
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site"),
        query_params={"region_id": "$region"},
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location"),
        query_params={"site_id": "$site"},
    )

    asset_group = DynamicModelChoiceField(
        required=False,
        label=_("Asset Group"),
        queryset=AssetGroup.objects.all(),
    )

    manufacturer = forms.CharField(
        required=False,
        label=_("Manufacturer"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter manufacturer")}
        )
    )

    device_type = forms.CharField(
        required=False,
        label=_("Device Type"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter device type")}
        )
    )

    tag = TagFilterField(model=Asset)

    fieldsets = (
        FieldSet("q", name=_("Search")),
        FieldSet(
            "name",
            "status",
            "region",
            "site",
            "location",
            "asset_group",
            "manufacturer",
            "device_type",
            "tag",
            name=_("Asset Filter"),
        ),
    )
    

class AssetForm(NetBoxModelForm):

    attachment = MultipleFileField(
        required=False,
        label=_("New Attachment"),
        help_text=_("Only jpg, jpeg, png allowed. Maximum total size per file: 25MB."),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
        widget=CustomUploadWidget(
            attrs={
                "multiple": True
            }
        ),
    )

    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site"),
        query_params={
            "region_id": "$region"
        }
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location"),
        query_params={
            "site_id": "$site"
        }
    )

    installation_date = forms.DateField(
        required=False,
        label=_("Installation Date"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    purchase_date = forms.DateField(
        required=False,
        label=_("Purchase Date"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    warranty_expiration_date = forms.DateField(
        required=False,
        label=_("Warranty Expiration Date"),
        disabled=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
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
            "installation_date",
            "purchase_date",
            "warranty_period_months",
            "attachment",
            "region",
            "site",
            "location",
            "tags",
        )

        labels = {
            "name": _("Name"),
            "code": _("Code"),
            "asset_group": _("Asset Group"),
            "status": _("Status"),
            "description": _("Description"),
            "device_type": _("Device Type"),
            "model": _("Model"),
            "serial": _("Serial"),
            "manufacturer": _("Manufacturer"),
            "installation_date": _("Installation Date"),
            "purchase_date": _("Purchase Date"),
            "warranty_period_months": _("Warranty Period (months)"),
            "warranty_expiration_date": _("Warranty Expiration Date"),
            "attachment": _("Attachment"),
            "region": _("Region"),
            "site": _("Site"),
            "location": _("Location"),
        }

        help_texts = {
            "name": _("Maximum 100 characters."),
            "code": _("Maximum 50 characters and must be unique."),
            "description": _("Maximum 500 characters."),
            "attachment": _("Only jpg, jpeg, png allowed. Maximum size 25MB."),
            "device_type": _("Maximum 100 characters."),
            "warranty_period_months": _("Enter a positive integer (unit: months)."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["asset_group"].queryset = AssetGroup.objects.filter(
            status="active"
        )
        if self.instance and self.instance.pk:
            self.fields["warranty_expiration_date"].initial = (
                self.instance.warranty_expiration_date
            )

    def clean_attachment(self):
        files = self.files.getlist("attachment")

        if not files:
            return []

        allowed_extensions = {"jpg", "jpeg", "png"}
        max_size = 25 * 1024 * 1024

        for file in files:
            if file.size > max_size:
                raise forms.ValidationError(
                    _("File '%(name)s' exceeds 25MB.") % {"name": file.name}
                )
            extension = file.name.rsplit(".", 1)[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    _("File '%(name)s' has unsupported extension.") % {"name": file.name}
                )

        return files


class AssetEditForm(NetBoxModelForm):

    attachment = MultipleFileField(
        required=False,
        label=_("New Attachment"),
        help_text=_("Only jpg, jpeg, png allowed. Maximum total size per file: 25MB."),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
        widget=CustomUploadWidget(
            attrs={
                "multiple": True
            }
        ),
    )

    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        label=_("Region")
    )

    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        label=_("Site"),
        query_params={
            "region_id": "$region"
        }
    )

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label=_("Location"),
        query_params={
            "site_id": "$site"
        }
    )

    installation_date = forms.DateField(
        required=False,
        label=_("Installation Date"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    purchase_date = forms.DateField(
        required=False,
        label=_("Purchase Date"),
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    warranty_expiration_date = forms.DateField(
        required=False,
        label=_("Warranty Expiration Date"),
        disabled=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
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
            "installation_date",
            "purchase_date",
            "warranty_period_months",
            "region",
            "site",
            "location",
            "tags",
        )

        labels = {
            "name": _("Name"),
            "code": _("Code"),
            "asset_group": _("Asset Group"),
            "status": _("Status"),
            "description": _("Description"),
            "device_type": _("Device Type"),
            "model": _("Model"),
            "serial": _("Serial"),
            "manufacturer": _("Manufacturer"),
            "installation_date": _("Installation Date"),
            "purchase_date": _("Purchase Date"),
            "warranty_period_months": _("Warranty Period (months)"),
            "warranty_expiration_date": _("Warranty Expiration Date"),
            "attachment": _("New Attachment"),
            "region": _("Region"),
            "site": _("Site"),
            "location": _("Location"),
        }

        help_texts = {
            "name": _("Maximum 100 characters."),
            "code": _("Maximum 50 characters and must be unique."),
            "description": _("Maximum 500 characters."),
            "attachment": _("Upload a new attachment to replace the selected one. Allowed file types: JPG, JPEG, PNG. Maximum size: 25MB."),
            "device_type": _("Maximum 100 characters."),
            "warranty_period_months": _("Enter a positive integer (unit: months)."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["asset_group"].queryset = AssetGroup.objects.filter(
            status="active"
        )
        if self.instance and self.instance.pk:
            self.fields["warranty_expiration_date"].initial = (
                self.instance.warranty_expiration_date
            )
            

    def clean_attachment(self):
        files = self.files.getlist("attachment")

        if not files:
            return []

        allowed_extensions = {"jpg", "jpeg", "png"}
        max_size = 25 * 1024 * 1024

        for file in files:
            if file.size > max_size:
                raise forms.ValidationError(
                    _("File '%(name)s' exceeds 25MB.") % {"name": file.name}
                )
            extension = file.name.rsplit(".", 1)[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    _("File '%(name)s' has unsupported extension.") % {"name": file.name}
                )

        return files
    
    

    


    
    
    
