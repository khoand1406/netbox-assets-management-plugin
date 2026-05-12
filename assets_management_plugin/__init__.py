"""
NetBox assets-management Plugin

Plugin configuration for NetBox assets-management Plugin.

For a complete list of PluginConfig attributes, see:
https://docs.netbox.dev/en/stable/plugins/development/#pluginconfig-attributes
"""

__author__ = """Khoa Nguyen"""
__email__ = "nguyenkhoa14022002@gmail.com"
__version__ = "0.1.0"


from netbox.plugins import PluginConfig


class AssetsmanagementConfig(PluginConfig):
    name = "assets_management_plugin"
    verbose_name = "NetBox assets-management Plugin"
    description = "NetBox plugin for assets-management."
    author= "Khoa Nguyen"
    author_email = "nguyenkhoa14022002@gmail.com"
    version = __version__
    base_url = "assets_management_plugin"
    min_version = "4.5.0"
    max_version = "4.5.99"
    graphql_schema = "graphql.schema"


config = AssetsmanagementConfig
