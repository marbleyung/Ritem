from .serializers import ImageSerializer
from rest_framework import generics, mixins, viewsets
from .models import Image
from rest_framework import permissions
from account.perms import IsObjectOwner
from .services import delete_image


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
