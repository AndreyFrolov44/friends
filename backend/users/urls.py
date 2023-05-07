from django.urls import path
from djoser.views import UserViewSet

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/me/', UserViewSet.as_view({'get': 'me'}), name='user-me'),
]