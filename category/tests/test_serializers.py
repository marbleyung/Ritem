from collections import OrderedDict
from collections.abc import ValuesView

from django.test import TestCase
from ..models import Category
from ..serializers import CategorySerializer


class CategorySerializerTestCase(TestCase):
    def test_ok(self):
        category1 = Category.objects.create(name='Test Category 1')
        category2 = Category.objects.create(name='Test Category 2', parent_id=1)
        category3 = Category.objects.create(name='Test Category 3')
        serializer_data = CategorySerializer([category1, category2, category3], many=True).data
        expected_data = [
            {
                'name': 'Test Category 1',
                'logo': None,
                'parent': category1.parent,
                'id': category1.id,
                'slug': category1.slug,
            },
            {
                'name': 'Test Category 2',
                'logo': None,
                'parent': 1,
                'id': category2.id,
                'slug': category2.slug,
            },
            {
                'name': 'Test Category 3',
                'logo': None,
                'parent': category3.parent,
                'id': category3.id,
                'slug': category3.slug,
            }
        ]
        self.assertEqual(expected_data, serializer_data)
