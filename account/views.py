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

    http_method_names = ['get', 'post', 'patch', 'delete']


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (permissions.IsAuthenticated,
                          IsUserSelfUser)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if old_password == new_password:
                return Response({"Error": ["Your new password can't be identical to your old password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            if len(new_password) < 8 or len(new_password) > 30 or new_password.isalpha() or new_password.isdigit():
                return Response({"Error": ["Password has to be 8...30 symbols"
                                           " and can't be made of letters or digits only."]},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(new_password)
            self.object.save()
            response = {
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
