"""
Navigation menu items for NetBox assets-management Plugin.

For more information on navigation menus, see:
https://docs.netbox.dev/en/stable/plugins/development/navigation/
"""

from netbox.plugins.navigation import PluginMenu
from netbox.plugins import PluginMenuButton, PluginMenuItem
from django.utils.translation import gettext_lazy as _

menu = PluginMenu(
    label=_('Assess Group'),                   
    groups=(                            
        (
            _('Management'),         
            (
                PluginMenuItem(
                    link='plugins:assets_management_plugin:assetgroup_list',
                    link_text=_('Assess Groups'),
                    buttons=(
                        PluginMenuButton(
                            link='plugins:assets_management_plugin:assetgroup_add',
                            title=_('Add Assess Group'),
                            icon_class='mdi mdi-plus-thick',
                            permissions=['assets_management_plugin.add_assetgroup'],
                        ),
                    )
                ),
                PluginMenuItem(
                    link='plugins:assets_management_plugin:asset_list',
                    link_text=_('Assets'),
                ),
            ),
        ),
        
    ),
    icon_class='mdi mdi-package-variant'  # Icon Material Design
)