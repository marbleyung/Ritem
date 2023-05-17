from rest_framework import viewsets, mixins
from rest_framework import permissions
from .serializers import *
from .models import UserItemRelation


class UserItemRelationView(viewsets.GenericViewSet,
                           mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserItemRelation.objects.all()
    serializer_class = UserItemRelationSerializer
    lookup_field = 'item'

    def get_object(self):
        obj, _ = UserItemRelation.objects.get_or_create(
            user=self.request.user,
            item_id=self.kwargs['item'])
        return obj