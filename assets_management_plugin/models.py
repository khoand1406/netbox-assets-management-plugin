"""
Models for NetBox assets-management Plugin.

For more information on NetBox models, see:
https://docs.netbox.dev/en/stable/plugins/development/models/

For NetBox model features (tags, custom fields, change logging, etc.), see:
https://docs.netbox.dev/en/stable/development/models/#netbox-model-features
"""

from django.db import models
from django.urls import reverse
from dcim.models.sites import Location, Region, Site
from netbox.models import NetBoxModel
from django.core.exceptions import ValidationError

from netbox import settings
from netbox.models.features import ImageAttachmentsMixin
from .choices import AssetStatusChoices, AssetsManagemnentChoice
from django.core.validators import MinValueValidator


class Assetsmanagement(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = "assets_management_plugin"
        ordering = ("name",)
        verbose_name_plural = "Assets Groups"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_asset_groups:assetsmanagementt", args=[self.pk])

class AssetGroup(ImageAttachmentsMixin, NetBoxModel):
    """
    Model representing a group of assets.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Asset Group Name",
        help_text="The name of the asset group."
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Asset Group Code",
        help_text="A unique identifier for the asset group."
    )

    status = models.CharField(
        max_length=20,
        choices=AssetsManagemnentChoice,
        default=AssetsManagemnentChoice.STATUS_ACTIVE,
        verbose_name="Status",
        help_text="The current status of the asset group."
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Detailed description of the asset group."
    )
    
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    
    excluded_from_visualization= models.BooleanField(
        default=False,
        verbose_name="Exclude from Visualization",
        help_text="If enabled, this asset group will be excluded from visualizations and reports."
    )

    class Meta:
        ordering = ("-last_updated",)
        verbose_name = "Asset Group"
        verbose_name_plural = "Asset Groups"

    
    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse(
        "plugins:assets_management_plugin:assetgroup",
        args=[self.pk]
    )

    def get_status_color(self):
        """
        Return the Bootstrap color associated with the current status.
        """
        return AssetsManagemnentChoice.COLOR_MAP.get(
            self.status,
            "secondary"
        )
        
class Asset(ImageAttachmentsMixin, NetBoxModel):
    

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Name"
    )

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code"
    )

    asset_group = models.ForeignKey(
        AssetGroup,
        on_delete=models.PROTECT,
        related_name="assets",
        limit_choices_to={"status": "active"},
        verbose_name="Asset Group"
    )

    status = models.CharField(
        max_length=30,
        choices=AssetStatusChoices,
        default=AssetStatusChoices.ACTIVE,
        verbose_name="Status"
    )

    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Description"
    )

    device_type = models.CharField(
        max_length=100,
        verbose_name="Device Type"
    )

    model = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Model"
    )

    serial = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Serial"
    )

    manufacturer = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Manufacturer"
    )
    
    created_by= models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    installation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Installation Date"
    )

    purchase_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Purchase Date"
    )

    warranty_period_months = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name="Warranty Period (months)"
    )

    warranty_expiration_date = models.DateField(
        blank=True,
        null=True,
        editable=False,
        verbose_name="Warranty Expiration Date"
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="assets",
        blank=True,
        null=True,
        verbose_name="Region"
    )

    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="assets",
        blank=True,
        null=True,
        verbose_name="Site"
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="assets",
        blank=True,
        null=True,
        verbose_name="Location"
    )

    class Meta:
        ordering = ("-last_updated",)
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse(
            "plugins:assets_management_plugin:asset",
            args=[self.pk]
        )
    
    def get_status_color(self):
        """
        Return the Bootstrap color associated with the current status.
        """
        return AssetStatusChoices.COLOR_MAP.get(
            self.status,
            "secondary"
        )

    def clean(self):
        
        super().clean()

      
        if self.site and self.region and self.site.region_id != self.region_id:
            raise ValidationError({
                "site": "Site does not belong to the selected Region."
            })

       
        if self.location and self.site and self.location.site_id != self.site_id:
            raise ValidationError({
                "location": "Location does not belong to the selected Site."
            })

        
        if self.purchase_date and self.warranty_period_months:
            from dateutil.relativedelta import relativedelta
            self.warranty_expiration_date = (
                self.purchase_date
                + relativedelta(months=self.warranty_period_months)
            )
        else:
            self.warranty_expiration_date = None