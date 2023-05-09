from rest_framework.response import Response

from .serializers import *
from rest_framework import viewsets, mixins, permissions, parsers, generics, status
from .models import *
from .perms import IsUserSelfUser, IsObjectOwner
from .services import delete_user_image


class UserImageView(viewsets.ModelViewSet):
    serializer_class = UserImageSerializer
    queryset = UserImage.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsObjectOwner]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser,
                      parsers.JSONParser)

    def update(self, request, *args, **kwargs):
        return Response({'message': 'Use POST to create new Image object'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        user = self.request.user
        delete_user_image(user)
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        delete_user_image(self.request.user)


class UserProfileView(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsUserSelfUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer, **kwargs):
        serializer.save()
