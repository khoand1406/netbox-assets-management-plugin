from utilities.choices import ChoiceSet
from django.utils.translation import gettext_lazy as _

class AssetsManagemnentChoice(ChoiceSet):
    """
    Choices for Assets Management Plugin
    """
    
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"

    CHOICES = (
        (STATUS_ACTIVE, _("Active")),
        (STATUS_INACTIVE, _("Inactive")),
    )

    COLOR_MAP = {
        STATUS_ACTIVE: "success",
        STATUS_INACTIVE: "warning",
    }

class AssetStatusChoices(ChoiceSet):
    
    key = "Asset.status"
    
    ACTIVE = "active"
    STANDBY = "standby"
    MAINTENANCE = "maintenance"
    BROKEN = "broken"

    CHOICES = [
        ("active", _("Active"), "green"),
        ("standby", _("Standby"), "blue"),
        ("maintenance", _("Maintenance"), "yellow"),
        ("broken", _("Broken"), "red"),
    ]
    
    COLOR_MAP = {
        ACTIVE: "success",
        STANDBY: "primary",
        MAINTENANCE: "warning",
        BROKEN: "danger",
    }
    