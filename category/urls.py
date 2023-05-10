from .views import *
from django.urls import path


app_name = 'category'
urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
]
