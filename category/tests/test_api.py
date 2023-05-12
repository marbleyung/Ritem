from rest_framework.test import APITestCase
from django.urls import reverse, reverse_lazy

from account.models import CustomUser
from ..models import Category, Tag
from ..serializers import CategorySerializer, TagSerializer
from rest_framework import status


class CategoriesListTestCase(APITestCase):
    url = reverse('category:categories')

    def test_get(self):
        category1 = Category.objects.create(name='Test Category 1')
        category2 = Category.objects.create(name='Test Category 2', parent_id=1)
        category3 = Category.objects.create(name='Test Category 3')
        response = self.client.get(self.url)
        serializer_data = CategorySerializer([category1, category2, category3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        data = {'name': 'Test Category 1'}
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        post_response = self.client.post(self.url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, post_response.status_code)
        get_response = self.client.get(self.url)
        self.assertEqual(post_response.data, get_response.data[0])


class CategoryDetailTestCase(APITestCase):
    url1 = reverse('category:category', kwargs={'pk': 5})
    url2 = reverse('category:category', kwargs={'pk': 6})
    url3 = reverse('category:category', kwargs={'pk': 7})

    def test_get(self):
        response1 = self.client.get(self.url1)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response1.status_code)

        category1 = Category.objects.create(name='Test Category 1')
        category2 = Category.objects.create(name='Test Category 2')
        response1 = self.client.get(self.url1)
        response2 = self.client.get(self.url2)

        serializer1 = CategorySerializer(category1).data
        serializer2 = CategorySerializer(category2).data

        self.assertEqual(status.HTTP_200_OK, response1.status_code)
        self.assertEqual(status.HTTP_200_OK, response2.status_code)
        self.assertEqual(serializer1, response1.data)
        self.assertEqual(serializer2, response2.data)

    def test_post(self):
        response = self.client.post(self.url1)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_put(self):
        response = self.client.put(self.url1)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

