"""
Forms for NetBox assets-management Plugin.

For more information on NetBox forms, see:
https://docs.netbox.dev/en/stable/plugins/development/forms/
"""
from django import forms
from dcim.models.sites import Location
from dcim.models.sites import Region, Site
from extras.models.models import ImageAttachment
from netbox.forms import NetBoxModelForm
from django.core.validators import FileExtensionValidator
from netbox.forms.bulk_edit import NetBoxModelBulkEditForm
from netbox.forms.bulk_import import PrimaryModelImportForm
from utilities.forms.fields.csv import CSVModelChoiceField
from utilities.forms.fields import DynamicModelChoiceField
from netbox.forms.filtersets import NetBoxModelFilterSetForm
from utilities.forms.fields import TagFilterField
from utilities.forms.rendering import FieldSet
from django.contrib.contenttypes.models import ContentType
from .choices import AssetStatusChoices, AssetsManagemnentChoice

from .models import Asset, AssetGroup, Assetsmanagement
 

class AssetsmanagementForm(NetBoxModelForm):
    class Meta:
        model = Assetsmanagement
        fields = ("name", "tags")
        
class AssetGroupForm(NetBoxModelForm):
    """
    Form thêm mới/chỉnh sửa Asset Group.
    """
    attachment = forms.ImageField(
        required=False,
        label="Attachment",
        help_text="Only jpg, jpeg, png allowed. Maximum size 25MB.",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
    )

    class Meta:
        model = AssetGroup
        fields = (
            "name",
            "code",
            "status",
            "description",
            "excluded_from_visualization",
            "attachment",
        )

        labels = {
            "name": "Name",
            "code": "Code",
            "status": "Status",
            "description": "Description",
            "exclude_from_visualization": "Exclude from Visualization",
            "attachment": "Attachment",
        }

        help_texts = {
            "name": "Allow up to 100 characters.",
            "code": "Allow up to 50 characters. Unique value.",
            "status": "Default is Active.",
            "description": "Allow up to 500 characters.",
            "exclude_from_visualization": (
                "When selected, assets in this group will not be "
                "included in the visualization."
            ),
            "attachment": "Only jpg, jpeg, png allowed. Maximum size 25MB.",
        }

    def clean_attachment(self):
        """
        Kiểm tra dung lượng file upload tối đa 25MB.
        """
        file = self.cleaned_data.get("attachment")

        if file and file.size > 25 * 1024 * 1024:
            raise forms.ValidationError(
                "File size cannot exceed 25MB."
            )

        return file
    
class AssetGroupEditForm(NetBoxModelForm):
    
    image_attachment = forms.ModelChoiceField(
        queryset=ImageAttachment.objects.none(),
        required=False,
        label="Attachments",
        help_text=(
            "Select an existing attachment to update. "
            "Leave blank to create a new attachment."
        ),
    )

    # Upload ảnh mới
    attachment = forms.ImageField(
        required=False,
        label="New Attachment",
        help_text=(
            "Upload a new attachment to replace the selected one. "
            "Allowed file types: JPG, JPEG, PNG. Maximum size: 25MB."
        ),
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
    )

    class Meta:
        model = AssetGroup
        fields = (
            "name",
            "code",
            "status",
            "description",
            "image_attachment",          
            "attachment",
            "excluded_from_visualization",
        )

        labels = {
            "name": "Name",
            "code": "Code",
            "status": "Status",
            "description": "Description",
            "image_attachment": "Attachments",
            "attachment": "New Attachment",
            "excluded_from_visualization": "Exclude from Visualization",
        }

        help_texts = {
            "name": "Allow up to 100 characters.",
            "code": "Allow up to 50 characters. Unique value.",
            "status": "Default is Active.",
            "description": "Allow up to 500 characters.",
            "excluded_from_visualization": (
                "When selected, assets in this group will not be "
                "included in the visualization."
            ),
            "attachment": "Upload a new attachment to replace the selected one. Allowed file types: JPG, JPEG, PNG. Maximum size: 25MB.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        if self.instance and self.instance.pk:
            content_type = ContentType.objects.get_for_model(self.instance)

            images = ImageAttachment.objects.filter(
                object_type=content_type,
                object_id=self.instance.pk
            ).order_by("-created")

            
            self.fields["image_attachment"].queryset = images

            
            self.fields["image_attachment"].label_from_instance = (
                lambda obj: (
                    f"{obj.name or obj.image.name} "
                    f"(ID: {obj.pk})"
                )
            )

            
            if images.exists():
                self.fields["image_attachment"].initial = images.first()
              
class AssetGroupFilterForm(NetBoxModelFilterSetForm):
    model = AssetGroup

    name = forms.CharField(
        required=False,
        label="Tên",
        widget=forms.TextInput(
            attrs={"placeholder": "Nhập tên nhóm"}
        )
    )

    status = forms.MultipleChoiceField(
        choices=AssetGroup._meta.get_field("status").choices,
        required=False,
        label="Trạng thái",
    )

    class Meta:
        model = AssetGroup
        fields = ("q", "name", "status")

    fieldsets = (
        
        FieldSet("q"),

        
        FieldSet("name", "status", name="Asset Group"),
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
    
    
class AssetFilterForm(NetBoxModelFilterSetForm):
    model = Asset

    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name, code, description, manufacturer, or device type"
            }
        )
    )

    name = forms.CharField(
        required=False,
        label="Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter asset name"
            }
        )
    )

    status = forms.MultipleChoiceField(
        required=False,
        label="Status",
        choices=Asset._meta.get_field("status").choices,
    )

    location = forms.ModelChoiceField(
        required=False,
        label="Location",
        queryset=Location.objects.all(),
    )

    asset_group = forms.ModelChoiceField(
        required=False,
        label="Asset Group",
        queryset=AssetGroup.objects.all(),
    )

    manufacturer = forms.CharField(
        required=False,
        label="Manufacturer",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter manufacturer"
            }
        )
    )

    device_type = forms.CharField(
        required=False,
        label="Device Type",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter device type"
            }
        )
    )

    class Meta:
        model = Asset
        fields = (
            "q",
            "name",
            "status",
            "location",
            "asset_group",
            "manufacturer",
            "device_type",
        )

    fieldsets = (
        FieldSet("q", name="Tìm kiếm"),
        FieldSet(
            "name",
            "status",
            "asset_group",
            "location",
            "manufacturer",
            "device_type",
            name="Bộ lọc tài sản",
        ),
    )
    
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

class AssetForm(NetBoxModelForm):
    
    attachment= forms.ImageField(
        required=False,
        label="Attachment",
        help_text="Only jpg, jpeg, png allowed. Maximum size 25MB.",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
    )
    
    region= DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required= False,
        label= "Region"
        
    )
    
    site= DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required= False,
        label="Site",
        query_params={
            "region_id":"$region"
        }
    )
    location= DynamicModelChoiceField(
        queryset= Location.objects.all(),
        required= False,
        label= "Location",
        query_params={
            "site_id":"$site"
        }
    )
    
    installation_date = forms.DateField(
        required=False,
        label="Installation Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    purchase_date = forms.DateField(
        required=False,
        label="Purchase Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    warranty_expiration_date = forms.DateField(
        required=False,
        label="Warranty Expiration Date",
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
            "name": "Name",
            "code": "Code",
            "asset_group": "Asset Group",
            "status": "Status",
            "description": "Description",
            "device_type": "Device Type",
            "model": "Model",
            "serial": "Serial",
            "manufacturer": "Manufacturer",
            "installation_date": "Installation Date",
            "purchase_date": "Purchase Date",
            "warranty_period_months": "Warranty Period (months)",
            "warranty_expiration_date": "Warranty Expiration Date",
            "attachment": "Attachment",
            "region": "Region",
            "site": "Site",
            "location": "Location",
        }

        help_texts = {
            "name": "Maximum 100 characters.",
            "code": "Maximum 50 characters and must be unique.",
            "description": "Maximum 500 characters.",
            "attachment": "Only jpg, jpeg, png allowed. Maximum size 25MB.",
            "device_type": "Maximum 100 characters.",
            "warranty_period_months": "Enter a positive integer (unit: months).",
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
        """
        Kiểm tra kích thước file tối đa 25MB.
        """
        file = self.cleaned_data.get("attachment")
        if file and file.size > 25 * 1024 * 1024:
            raise forms.ValidationError(
                "File size cannot exceed 25MB."
            )
        return file
    
class AssetEditForm(NetBoxModelForm):
    
    image_attachment= forms.ModelChoiceField(
        queryset=ImageAttachment.objects.none(),
        required=False,
        label="Attachments",
        help_text=(
            "Select an existing attachment to update. "
            "Leave blank to create a new attachment."
        ),
    )
    
    attachment= forms.ImageField(
        required=False,
        label="New Attachment",
        help_text="Only jpg, jpeg, png allowed. Maximum size 25MB.",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"]
            )
        ],
    )
    
    
    region= DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required= False,
        label= "Region"
        
    )
    
    site= DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required= False,
        label="Site",
        query_params={
            "region_id":"$region"
        }
    )
    location= DynamicModelChoiceField(
        queryset= Location.objects.all(),
        required= False,
        label= "Location",
        query_params={
            "site_id":"$site"
        }
    )
    
    installation_date = forms.DateField(
        required=False,
        label="Installation Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    purchase_date = forms.DateField(
        required=False,
        label="Purchase Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "placeholder": "DD/MM/YYYY",
            }
        ),
    )

    warranty_expiration_date = forms.DateField(
        required=False,
        label="Warranty Expiration Date",
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
            
            "image_attachment",
            "attachment",
            "region",
            "site",
            "location",
            "tags",
        )

        labels = {
            "name": "Name",
            "code": "Code",
            "asset_group": "Asset Group",
            "status": "Status",
            "description": "Description",
            "device_type": "Device Type",
            "model": "Model",
            "serial": "Serial",
            "manufacturer": "Manufacturer",
            "installation_date": "Installation Date",
            "purchase_date": "Purchase Date",
            "warranty_period_months": "Warranty Period (months)",
            "warranty_expiration_date": "Warranty Expiration Date",
            "image_attachment":"Attachments",
            "attachment": "New Attachment",
            "region": "Region",
            "site": "Site",
            "location": "Location",
        }

        help_texts = {
            "name": "Maximum 100 characters.",
            "code": "Maximum 50 characters and must be unique.",
            "description": "Maximum 500 characters.",
            "attachment": "Upload a new attachment to replace the selected one. Allowed file types: JPG, JPEG, PNG. Maximum size: 25MB.",
            "device_type": "Maximum 100 characters.",
            "warranty_period_months": "Enter a positive integer (unit: months).",
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
            content_type= ContentType.objects.get_for_model(self.instance)
            images = ImageAttachment.objects.filter(
                object_type=content_type,
                object_id=self.instance.pk
            ).order_by("-created")
            self.fields["image_attachment"].queryset = images

            self.fields["image_attachment"].label_from_instance = (
                lambda obj: (
                    f"{obj.name or obj.image.name} "
                    f"(ID: {obj.pk})"
                )
            )
            if images.exists():
                self.fields["image_attachment"].initial = images.first()


    def clean_attachment(self):
        """
        Kiểm tra kích thước file tối đa 25MB.
        """
        file = self.cleaned_data.get("attachment")
        if file and file.size > 25 * 1024 * 1024:
            raise forms.ValidationError(
                "File size cannot exceed 25MB."
            )
        return file
    
    
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

    


    
    
    
