from .views import *
from django.urls import path


app_name = 'category'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('tags/', TagListView.as_view()),
    path('tag/<int:pk>/', TagDetailView.as_view()),
]
