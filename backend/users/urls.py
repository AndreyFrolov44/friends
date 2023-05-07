from django.urls import path
from djoser.views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'post': 'create'}), name='user-list'),
]