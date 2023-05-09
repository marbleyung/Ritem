from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

from .models import CustomUser


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(Q(email=username) | Q(username=username))
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
        except MultipleObjectsReturned:
            return CustomUser.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
