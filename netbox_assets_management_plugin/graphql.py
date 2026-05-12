"""
GraphQL schema for NetBox assets-management Plugin.

For more information on NetBox GraphQL, see:
https://docs.netbox.dev/en/stable/plugins/development/graphql/

For Strawberry GraphQL documentation, see:
https://strawberry.rocks/
"""

from typing import List

import strawberry
import strawberry_django

from .models import Assetsmanagement


@strawberry_django.type(
    Assetsmanagement,
    fields='__all__',
)
class AssetsmanagementType:
    """GraphQL type for Assetsmanagement model."""
    pass


@strawberry.type(name="Query")
class AssetsmanagementQuery:
    """GraphQL queries for NetBox assets-management Plugin."""

    assetsmanagement: AssetsmanagementType = strawberry_django.field()
    assetsmanagement_list: List[AssetsmanagementType] = strawberry_django.field()


schema = [
    AssetsmanagementQuery,
]

