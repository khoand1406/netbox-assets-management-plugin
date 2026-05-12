"""
Test cases for NetBox assets-management Plugin GraphQL API.
"""
from ..models import Assetsmanagement
from ..testing import PluginGraphQLTestCase


class AssetsmanagementGraphQLTestCase(PluginGraphQLTestCase):
    """Test Assetsmanagement GraphQL queries."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Assetsmanagement.objects.create(name='GraphQL Test 1')
        Assetsmanagement.objects.create(name='GraphQL Test 2')
        Assetsmanagement.objects.create(name='GraphQL Test 3')

    def test_query_assetsmanagement(self):
        """Test GraphQL query for a single Assetsmanagement."""
        self.add_permissions('netbox_assets_management_plugin.view_assetsmanagement')

        instance = Assetsmanagement.objects.first()

        query = (
            "query { "
            "assetsmanagement(id: " + str(instance.pk) + ") { "
            "id name "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['assetsmanagement']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)

    def test_query_assetsmanagement_list(self):
        """Test GraphQL query for list of Assetsmanagements."""
        self.add_permissions('netbox_assets_management_plugin.view_assetsmanagement')

        query = """
        query {
            assetsmanagement_list {
                id
                name
            }
        }
        """

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['assetsmanagement_list']
        self.assertEqual(len(data), 3)
        self.assertIn('id', data[0])
        self.assertIn('name', data[0])

    def test_query_assetsmanagement_with_all_fields(self):
        """Test GraphQL query with all available fields."""
        self.add_permissions('netbox_assets_management_plugin.view_assetsmanagement')

        instance = Assetsmanagement.objects.first()

        query = (
            "query { "
            "assetsmanagement(id: " + str(instance.pk) + ") { "
            "id name created last_updated "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['assetsmanagement']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)
        self.assertIsNotNone(data['created'])
        self.assertIsNotNone(data['last_updated'])

