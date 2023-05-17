from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from account.models import CustomUser
from item.models import Item
from category.models import Category, Tag


class UserItemRelationTestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(username='user1',
                                email='email1@mail.com')
        self.user2 = CustomUser.objects.create(username='user2',
                                email='email2@mail.com')
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')
        self.item1 = Item.objects.create(category=self.category1,
                                         name='Item 1',
                                         owner=self.user1)
        self.item2 = Item.objects.create(category=self.category2,
                                         name='Item 2',
                                         owner=self.user2)
        self.url1 = reverse('likes:relation')

    def test_get(self):
        response = self.client.get(self.url1)
        print(response)
