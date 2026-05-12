"""
Test cases for NetBox assets-management Plugin models.
"""

from django.core.exceptions import ValidationError

from ..models import Assetsmanagement
from ..testing import PluginModelTestCase
from ..testing.utils import create_tags, get_random_string


class AssetsmanagementTestCase(PluginModelTestCase):
    """Test Assetsmanagement model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        # Create test instances
        Assetsmanagement.objects.create(name='Test 1')
        Assetsmanagement.objects.create(name='Test 2')
        Assetsmanagement.objects.create(name='Test 3')

    def test_create_assetsmanagement(self):
        """Test creating a Assetsmanagement instance."""
        name = f'Test {get_random_string(10)}'
        instance = Assetsmanagement.objects.create(name=name)

        self.assertEqual(instance.name, name)
        self.assertIsNotNone(instance.pk)

    def test_assetsmanagement_str(self):
        """Test Assetsmanagement string representation."""
        instance = Assetsmanagement.objects.first()
        self.assertEqual(str(instance), instance.name)

    def test_assetsmanagement_absolute_url(self):
        """Test Assetsmanagement get_absolute_url method."""
        instance = Assetsmanagement.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_assetsmanagement_unique_name(self):
        """Test that Assetsmanagement names must be unique."""
        name = 'Duplicate Name'
        Assetsmanagement.objects.create(name=name)

        with self.assertRaises(ValidationError):
            instance = Assetsmanagement(name=name)
            instance.full_clean()

    def test_model_to_dict(self):
        """Test model_to_dict helper method."""
        instance = Assetsmanagement.objects.first()
        data = self.model_to_dict(instance)

        self.assertIn('name', data)
        self.assertEqual(data['name'], instance.name)
        self.assertIn('id', data)

    def test_instance_equal(self):
        """Test assertInstanceEqual helper method."""
        instance = Assetsmanagement.objects.first()

        # Should pass with matching data
        self.assertInstanceEqual(
            instance,
            {'name': instance.name, 'id': instance.pk}
        )

    def test_assetsmanagement_with_tags(self):
        """Test Assetsmanagement with tags."""
        tags = create_tags(['important', 'test'])
        instance = Assetsmanagement.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_bulk_create(self):
        """Test bulk creation of Assetsmanagement instances."""
        initial_count = Assetsmanagement.objects.count()

        instances = [
            Assetsmanagement(name=f'Bulk {i}')
            for i in range(5)
        ]
        Assetsmanagement.objects.bulk_create(instances)

        self.assertEqual(
            Assetsmanagement.objects.count(),
            initial_count + 5
        )

    def test_query_filter(self):
        """Test filtering Assetsmanagement instances."""
        # Create a specific instance for filtering
        test_name = f'FilterTest {get_random_string(10)}'
        Assetsmanagement.objects.create(name=test_name)

        # Test filter
        results = Assetsmanagement.objects.filter(name=test_name)
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, test_name)

    def test_ordering(self):
        """Test Assetsmanagement default ordering."""
        instances = list(Assetsmanagement.objects.all())

        # Check that instances are ordered by name
        names = [instance.name for instance in instances]
        self.assertEqual(names, sorted(names))


class AssetsmanagementValidationTestCase(PluginModelTestCase):
    """Test Assetsmanagement validation."""

    def test_empty_name(self):
        """Test that empty name is not allowed."""
        with self.assertRaises(ValidationError):
            instance = Assetsmanagement(name='')
            instance.full_clean()

    def test_name_max_length(self):
        """Test name field max length."""
        long_name = 'x' * 101  # Exceeds max_length of 100

        with self.assertRaises(ValidationError):
            instance = Assetsmanagement(name=long_name)
            instance.full_clean()
