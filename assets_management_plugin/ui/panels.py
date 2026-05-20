from netbox.ui.panels import Panel
from django.utils.translation import gettext_lazy as _
from upload_file_plugin.models import UploadedFile
from netbox.ui import attrs
from netbox.ui import panels
from netbox.ui import actions


class AssetsGroupPanel(panels.ObjectAttributesPanel):
    name = _("Detailed Information")
    slug = "asset_group_details"

    name_attr = attrs.TextAttr("name", label=_("Name"))
    code = attrs.TextAttr("code", label=_("Code"))
    status = attrs.ChoiceAttr("status", label=_("Status"))
    description = attrs.TextAttr("description", label=_("Description"))
    excluded_from_visualization = attrs.BooleanAttr("excluded_from_visualization", label=_("Excluded from Visualization"))
    created_by = attrs.RelatedObjectAttr("created_by", linkify=True, label=_("Created By"))
    created = attrs.DateTimeAttr("created", label=_("Created"))
    last_updated = attrs.DateTimeAttr("last_updated", label=_("Last Updated"))
    
class CustomImageAttachmentsPanel(Panel):
    title= _("Attachments")
    template_name= "assets_management_plugin/panels/custom_image_panel.html"
    actions = [
        actions.LinkAction(
            view_name="plugins:assets_management_plugin:uploadedfile_add",
            label= _("New Attachment"),
            button_icon= "plus-thick",
            permissions=["upload_file_plugin.add_uploadedfile"],
            
            url_params= {
                "object_id": lambda ctx: ctx["object"].pk,
                "model_name": lambda ctx: ctx["object"]._meta.model_name,
                "return_url": lambda ctx: ctx["object"].get_absolute_url(),
            },
        )
    ]

    def get_context(self, context):
        obj= context["object"]
        print(obj.pk)
        uploaded_files= UploadedFile.objects.filter(
            model_name= obj._meta.model_name,
            object_id= obj.pk
        ).order_by("-created_at")
        return {
            **super().get_context(context),
            "uploaded_files": uploaded_files,
            "object": obj,
            "model_name":obj._meta.model_name
        }
        
    
class AssetPanel(panels.ObjectAttributesPanel):
    name = _("Detailed Information")
    slug = "asset_details"

    name_attr = attrs.TextAttr("name", label=_("Name"))
    code = attrs.TextAttr("code", label=_("Code"))
    status = attrs.ChoiceAttr("status", label=_("Status"))
    site = attrs.RelatedObjectAttr("site", linkify=True, label=_("Site"))
    location = attrs.RelatedObjectAttr("location", linkify=True, label=_("Location"))
    asset_group = attrs.RelatedObjectAttr("asset_group", linkify=True, label=_("Asset Group"))
    manufacturer = attrs.TextAttr("manufacturer", label=_("Manufacturer"))
    device_type = attrs.TextAttr("device_type", label=_("Device Type"))
    installation_date = attrs.TextAttr("installation_date", label=_("Installation Date"))
    purchase_date = attrs.TextAttr("purchase_date", label=_("Purchase Date"))
    warranty_period_months = attrs.NumericAttr("warranty_period_months", label=_("Warranty Period (months)"))
    warranty_expiration_date = attrs.TextAttr("warranty_expiration_date", label=_("Warranty Expiration Date"))
    created_by = attrs.RelatedObjectAttr("created_by", linkify=True, label=_("Created By"))
    created = attrs.DateTimeAttr("created", label=_("Created"))
    last_updated = attrs.DateTimeAttr("last_updated", label=_("Last Updated"))
    