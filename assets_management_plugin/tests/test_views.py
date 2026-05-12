"""
Test cases for NetBox assets-management Plugin views.
"""

from django.urls import reverse

from ..models import Assetsmanagement
from ..testing import PluginViewTestCase
from ..testing.utils import disable_warnings, get_random_string


class AssetsmanagementViewTestCase(PluginViewTestCase):
    """Test Assetsmanagement views."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Assetsmanagement.objects.create(name='View Test 1')
        Assetsmanagement.objects.create(name='View Test 2')
        Assetsmanagement.objects.create(name='View Test 3')

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.base_url = 'plugins:assets_management_plugin:assetsmanagement'

    def test_list_assetsmanagements(self):
        """Test Assetsmanagement list view."""
        self.add_permissions('assets_management_plugin.view_assetsmanagement')

        url = reverse('plugins:assets_management_plugin:assetsmanagement_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_assetsmanagements_without_permission(self):
        """Test Assetsmanagement list view without permission."""
        url = reverse('plugins:assets_management_plugin:assetsmanagement_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_assetsmanagement(self):
        """Test Assetsmanagement detail view."""
        self.add_permissions('assets_management_plugin.view_assetsmanagement')

        instance = Assetsmanagement.objects.first()
        url = reverse('plugins:assets_management_plugin:assetsmanagement', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_assetsmanagement(self):
        """Test creating a Assetsmanagement via form."""
        self.add_permissions(
            'assets_management_plugin.add_assetsmanagement',
            'assets_management_plugin.view_assetsmanagement'
        )

        url = reverse('plugins:assets_management_plugin:assetsmanagement_add')
        name = f'Created {get_random_string(10)}'

        form_data = self.post_data({
            'name': name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was created
        instance = Assetsmanagement.objects.get(name=name)
        self.assertEqual(instance.name, name)

    def test_create_assetsmanagement_without_permission(self):
        """Test creating a Assetsmanagement without permission."""
        url = reverse('plugins:assets_management_plugin:assetsmanagement_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_assetsmanagement(self):
        """Test editing a Assetsmanagement via form."""
        self.add_permissions(
            'assets_management_plugin.change_assetsmanagement',
            'assets_management_plugin.view_assetsmanagement'
        )

        instance = Assetsmanagement.objects.first()
        url = reverse('plugins:assets_management_plugin:assetsmanagement_edit', kwargs={'pk': instance.pk})

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data({
            'name': new_name,
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was updated
        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)

    def test_delete_assetsmanagement(self):
        """Test deleting a Assetsmanagement."""
        self.add_permissions(
            'assets_management_plugin.delete_assetsmanagement',
            'assets_management_plugin.view_assetsmanagement'
        )

        instance = Assetsmanagement.objects.first()
        url = reverse('plugins:assets_management_plugin:assetsmanagement_delete', kwargs={'pk': instance.pk})

        # Confirm deletion
        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        # Verify object was deleted
        self.assertFalse(
            Assetsmanagement.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_assetsmanagement_without_permission(self):
        """Test deleting a Assetsmanagement without permission."""
        instance = Assetsmanagement.objects.first()
        url = reverse('plugins:assets_management_plugin:assetsmanagement_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)


class AssetsmanagementFormTestCase(PluginViewTestCase):
    """Test Assetsmanagement form validation."""

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions(
            'assets_management_plugin.add_assetsmanagement',
            'assets_management_plugin.view_assetsmanagement'
        )

    def test_form_validation_empty_name(self):
        """Test form validation with empty name."""
        url = reverse('plugins:assets_management_plugin:assetsmanagement_add')
        form_data = self.post_data({'name': ''})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should not create object
        self.assertEqual(Assetsmanagement.objects.filter(name='').count(), 0)

    def test_form_validation_duplicate_name(self):
        """Test form validation with duplicate name."""
        Assetsmanagement.objects.create(name='Duplicate')

        url = reverse('plugins:assets_management_plugin:assetsmanagement_add')
        form_data = self.post_data({'name': 'Duplicate'})

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)  # Form redisplay

        # Should only have one instance with this name
        self.assertEqual(Assetsmanagement.objects.filter(name='Duplicate').count(), 1)
