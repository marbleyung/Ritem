from .views import *
from django.urls import path


app_name = 'category'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag'),
]
