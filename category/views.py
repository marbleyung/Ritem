from rest_framework import generics, viewsets, mixins
from .models import Category, Tag
from .serializers import CategorySerializer, TagSerializer
from rest_framework import permissions
from . import perms


class CategoryListView(generics.ListAPIView,
                       generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [perms.IsModeratorOrReadOnly]


class CategoryDetailView(generics.RetrieveAPIView,
                         generics.UpdateAPIView,
                         generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [perms.IsModeratorOrReadOnly]

    http_method_names = ['get', 'patch', 'delete']


class TagListView(generics.ListAPIView,
                  generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [perms.IsModeratorOrReadOnly]


class TagDetailView(generics.RetrieveAPIView,
                    generics.UpdateAPIView,
                    generics.DestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [perms.IsModeratorOrReadOnly]

    http_method_names = ['get', 'patch', 'delete']
