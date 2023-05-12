from rest_framework.response import Response

from absconfig.settings import IMAGES_LIMIT_FOR_EACH_ITEM
from .serializers import *
from rest_framework import generics, mixins, viewsets
from .models import Image, Item
from rest_framework import permissions
from account.perms import IsObjectOwner
from .services import delete_image
from category.models import Tag
from .perms import IsOwnerOrReadOnly


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageRDView(generics.DestroyAPIView,
                  generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsObjectOwner]

    def delete(self, request, *args, **kwargs):
        image_item = Image.objects.get(pk=kwargs['pk']).item
        if image_item.count_images() == 1:
            return Response(data=
                            {'message':
                            'This item has only 1 image, the image cant be deleted'})
        delete_image(kwargs['pk'])
        return self.destroy(request, *args, **kwargs)


class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        images = self.request.FILES.getlist('image')
        item = serializer.save(owner=self.request.user)
        image_data = [{'image': image} for image in images]
        image_serializer = ImageSerializer(data=image_data, many=True)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save(owner=self.request.user, item=item)

        tags = self.request.POST.getlist('tags')
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            item.tags.add(tag)

        return item


class ItemListView(generics.ListAPIView):
    serializer_class = ItemGetSerializer
    queryset = Item.objects.all()


class ItemDetailView(generics.RetrieveAPIView,
                     generics.UpdateAPIView,
                     generics.DestroyAPIView):
    serializer_class = ItemGetSerializer
    queryset = Item.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ['get', 'patch', 'delete']

    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        item = Item.objects.get(pk=pk)
        count_images = item.count_images()
        limit = IMAGES_LIMIT_FOR_EACH_ITEM - count_images

        images = self.request.FILES.getlist('image')
        image_data = [{'image': image} for image in images[:limit]]
        image_serializer = ImageSerializer(data=image_data, many=True)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save(owner=self.request.user, item=item)

        tags = self.request.POST.getlist('tags')
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            item.tags.add(tag)
        serializer.save()

    def delete(self, request, *args, **kwargs):
        print(self.kwargs['pk'])
        images = Item.objects.get(pk=self.kwargs['pk']).images
        for image in images:
            delete_image(image.pk)

        return self.destroy(request, *args, **kwargs)
