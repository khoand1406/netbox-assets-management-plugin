from netbox.ui import attrs
from netbox.ui import panels


class AssetsGroupPanel(panels.ObjectAttributesPanel):
    """
    Panel hiển thị thông tin chi tiết của Asset Group.
    """

    
    name = "Thông tin chi tiết"

    
    slug = "asset_group_details"

    # Khai báo từng field giống cách NetBox định nghĩa SitePanel
    name_attr = attrs.TextAttr("name")
    code = attrs.TextAttr("code")
    status = attrs.ChoiceAttr("status")
    description = attrs.TextAttr("description")
    excluded_from_visualization = attrs.BooleanAttr("excluded_from_visualization")
    created_by = attrs.RelatedObjectAttr("created_by", linkify=True)
    created = attrs.DateTimeAttr("created")
    last_updated = attrs.DateTimeAttr("last_updated")
    
class AssetPanel(panels.ObjectAttributesPanel):
    """
    Panel hiển thị thông tin chi tiết của Asset.
    """
    name = "Thông tin chi tiết"

    slug = "asset_details"

    name_attr = attrs.TextAttr("name")
    code = attrs.TextAttr("code")
    status = attrs.ChoiceAttr("status")
    site = attrs.RelatedObjectAttr("site", linkify=True)
    location = attrs.RelatedObjectAttr("location", linkify=True)
    asset_group = attrs.RelatedObjectAttr("asset_group", linkify=True)
    manufacturer = attrs.TextAttr("manufacturer")
    device_type = attrs.TextAttr("device_type")
    installation_date = attrs.TextAttr("installation_date")
    purchase_date = attrs.TextAttr("purchase_date")
    warranty_period_months = attrs.NumericAttr("warranty_period_months")
    warranty_expiration_date = attrs.TextAttr("warranty_expiration_date")
    created_by = attrs.RelatedObjectAttr("created_by", linkify=True)
    created = attrs.DateTimeAttr("created")
    last_updated = attrs.DateTimeAttr("last_updated")
    