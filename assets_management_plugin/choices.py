from utilities.choices import ChoiceSet


class AssetsManagemnentChoice(ChoiceSet):
    """
    Choices for Assets Management Plugin
    """
    
    STATUS_ACTIVE = "active"
    STATUS_INACTIVE = "inactive"
    STATUS_ARCHIVED = "archived"

    CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_INACTIVE, "Inactive"),
        (STATUS_ARCHIVED, "Archived"),
    )

    COLOR_MAP = {
        STATUS_ACTIVE: "success",
        STATUS_INACTIVE: "warning",
        STATUS_ARCHIVED: "secondary",
    }

class AssetStatusChoices(ChoiceSet):
    
    key = "Asset.status"
    
    ACTIVE = "active"
    STANDBY = "standby"
    MAINTENANCE = "maintenance"
    BROKEN = "broken"

    CHOICES = [
        ("active", "Active", "green"),
        ("standby", "Standby", "blue"),
        ("maintenance", "Maintenance", "yellow"),
        ("broken", "Broken", "red"),
    ]
    
    COLOR_MAP = {
        ACTIVE: "success",
        STANDBY: "primary",
        MAINTENANCE: "warning",
        BROKEN: "danger",
    }
    