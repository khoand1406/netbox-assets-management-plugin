"""
Navigation menu items for NetBox assets-management Plugin.

For more information on navigation menus, see:
https://docs.netbox.dev/en/stable/plugins/development/navigation/
"""

from netbox.plugins.navigation import PluginMenu
from netbox.plugins import PluginMenuButton, PluginMenuItem

menu = PluginMenu(
    label='Assess Group',                    # Tên tab trên navigation bar
    groups=(                            # Các nhóm menu con
        (
            'Management',                  # Tên nhóm 1
            (
                PluginMenuItem(
                    link='plugins:netbox_assets_management_plugin:assetgroup_list',
                    link_text='Assess Groups',
                    permissions=['plugins:netbox_assets_management_plugin:assetgroup_list'],
                    buttons=(
                        PluginMenuButton(
                            link='plugins:netbox_assets_management_plugin:assetgroup_add',
                            title='Add Assess Group',
                            icon_class='mdi mdi-plus-thick',
                            permissions=['plugins:netbox_assets_management_plugin:assetgroup_add'],
                        ),
                    )
                ),
                PluginMenuItem(
                    link='plugins:netbox_assets_management_plugin:asset_list',
                    link_text='Assets',
                    permissions=['plugins:netbox_assets_management_plugin:asset_list'],
                ),
            ),
        ),
        
    ),
    icon_class='mdi mdi-package-variant'  # Icon Material Design
)