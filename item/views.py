from .serializers import *
from rest_framework import generics, mixins, viewsets
from .models import Image, Item
from rest_framework import permissions
from account.perms import IsObjectOwner
from .services import delete_image
from category.models import Tag


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
        delete_image(kwargs['pk'])
        return self.destroy(request, *args, **kwargs)


class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        images = self.request.FILES.getlist('image')
        tags = self.request.POST.getlist('tags')
        item = serializer.save()
        image_data = [{'image': image} for image in images]
        image_serializer = ImageSerializer(data=image_data, many=True)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save(owner=self.request.user, item=item)

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            item.tags.add(tag)

        return item


class ItemListView(generics.ListAPIView):
    serializer_class = ItemGetSerializer
    queryset = Item.objects.all()
