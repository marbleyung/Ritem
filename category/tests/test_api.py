from rest_framework.test import APITestCase
from django.urls import reverse

from account.models import CustomUser
from ..models import Category, Tag
from ..serializers import CategorySerializer, TagSerializer
from rest_framework import status


class CategoriesListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('category:categories')
        self.category1 = Category.objects.create(name='Test Category 1')
        self.category2 = Category.objects.create(name='Test Category 2',
                                                 parent_id=self.category1.id)
        self.category3 = Category.objects.create(name='Test Category 3')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = CategorySerializer([self.category1,
                                              self.category2,
                                              self.category3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        data = {'name': 'Test Category 4'}
        serializer = CategorySerializer(data=data)
        assert serializer.is_valid()
        post_response = self.client.post(self.url, data=data)
        self.assertEqual(status.HTTP_201_CREATED, post_response.status_code)
        get_response = self.client.get(self.url)
        self.assertEqual(post_response.data, get_response.data[3])


class CategoryDetailTestCase(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Test Category 1')
        self.category2 = Category.objects.create(name='Test Category 2')

        self.url1 = reverse('category:category',
                            kwargs={'pk': self.category1.pk})
        self.url2 = reverse('category:category',
                            kwargs={'pk': self.category2.pk})

        self.user1 = CustomUser.objects.create(username='testroot1',
                                               email='testroot1@mail.com',
                                               is_superuser=True)
        self.user2 = CustomUser.objects.create(username='testroot2',
                                               email='testroot2@mail.com',
                                               is_superuser=False)

    def test_get(self):

        response1 = self.client.get(self.url1)
        response2 = self.client.get(self.url2)

        serializer1 = CategorySerializer(self.category1).data
        serializer2 = CategorySerializer(self.category2).data

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

    def test_patch(self):
        self.client.force_login(self.user1)
        name = 'Test Category 1 upd'
        response_after_patch = self.client.patch(self.url1,
                                     data={'name': 'Test Category 1 upd'},
                                     )
        self.assertEqual(response_after_patch.data['name'], name)

    def test_patch_permission(self):
        self.client.force_login(self.user2)
        response_after_patch = self.client.patch(self.url1,
                                     data={'name': 'Test Category 1 upd'},
                                     )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response_after_patch.status_code)


class TagListTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('category:tags')
        self.tag1 = Tag.objects.create(name='Test Tag 1')
        self.tag2 = Tag.objects.create(name='Test Tag 2')
        self.tag3 = Tag.objects.create(name='Test Tag 3')

    def test_get(self):
        response = self.client.get(self.url)
        serializer_data = TagSerializer([self.tag1,
                                         self.tag2,
                                         self.tag3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        data = {'name': 'Test Tag 4'}
        post_response = self.client.post(self.url,
                                         data=data)
        self.assertEqual(status.HTTP_201_CREATED, post_response.status_code)
        get_response = self.client.get(self.url)
        self.assertEqual(post_response.data, get_response.data[3])


class TagDetailTestCase(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name='Test Tag 1')
        self.tag2 = Tag.objects.create(name='Test Tag 2')
        self.url1 = reverse('category:tag', args=(self.tag1.id, ))
        self.url2 = reverse('category:tag', args=(self.tag2.id, ))

        self.user1 = CustomUser.objects.create(username='testroot1',
                                               email='testroot1@mail.com',
                                               is_superuser=True)
        self.user2 = CustomUser.objects.create(username='testroot2',
                                               email='testroot2@mail.com',
                                               is_superuser=False)

    def test_get(self):
        response1 = self.client.get(self.url1)
        response2 = self.client.get(self.url2)
        self.assertEqual(status.HTTP_200_OK, response1.status_code)
        self.assertEqual(status.HTTP_200_OK, response2.status_code)

    def test_patch(self):
        self.client.force_login(self.user1)
        response = self.client.patch(self.url1, data={
            'name': 'Test Tag 1 upd'
        })
        get = self.client.get(self.url1)
        self.assertEqual(response.data['name'], get.data['name'])

    def test_delete(self):
        self.client.force_login(self.user1)
        delete = self.client.delete(self.url1)
        self.assertEqual(status.HTTP_204_NO_CONTENT, delete.status_code)

    def test_permissions(self):
        self.client.force_login(self.user2)
        delete = self.client.delete(self.url1)
        self.assertEqual(status.HTTP_403_FORBIDDEN, delete.status_code)

        patch = self.client.patch(self.url1,
                                  data={'name': 'Lorem'})
        self.assertEqual(status.HTTP_403_FORBIDDEN, patch.status_code)
