from django.urls import path, include

from .views import *
from rest_framework.routers import DefaultRouter

account_router = DefaultRouter()
account_router.register(r'profiles', UserProfileView, basename="profile")


urlpatterns = [
    path('avatar/set/', UserImageView.as_view({'post': 'create'})),
    path('avatar/delete/<int:pk>/', UserImageView.as_view({'delete': 'destroy'})),
    path('avatar/<int:pk>/', UserImageView.as_view({'get': 'retrieve'})),
    path('change-password/', ChangePasswordView.as_view()),
    path('', include(account_router.urls))
]
