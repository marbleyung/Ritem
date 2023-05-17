from django.urls import path
from .views import *


app_name = 'likes'

urlpatterns = [
    path('relation/', UserItemRelationView.as_view({'get': 'detail',
                                                    }), name='relation'),
]
