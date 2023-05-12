from django.urls import path
from .views import *

app_name = 'item'

urlpatterns = [
    path('upload-image/', ImageCreateView.as_view()),
    path('image/<int:pk>/', ImageRDView.as_view()),
    path('create-item/', ItemCreateView.as_view()),
    path('items/', ItemListView.as_view()),
    path('items/<int:pk>/', ItemDetailView.as_view()),
]
