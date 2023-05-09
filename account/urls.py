from django.urls import path, include

from .views import *
from rest_framework.routers import DefaultRouter

account_router = DefaultRouter()
account_router.register(r'profiles', UserProfileView, basename="profile")


urlpatterns = [
    path('avatar/<int:pk>/', UserImageView.as_view({'post': 'create',
                                                    'get': 'retrieve',
                                                    'put': 'update',
                                                    'delete': 'destroy'})),
    path('', include(account_router.urls))
]
