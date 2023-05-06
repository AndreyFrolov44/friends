from django.urls import path

from .views import RequestViewSet


urlpatterns = [
    path('', RequestViewSet.as_view({'post': 'create'}), name='sent_request'),
    path('accept/', RequestViewSet.as_view({'post': 'accept'}), name='accept_request'),
    path('reject/', RequestViewSet.as_view({'post': 'reject'}), name='reject_request'),
    path('outgoing/', RequestViewSet.as_view({'get': 'outgoing'}), name='outgoing_request'),
    path('incoming/', RequestViewSet.as_view({'get': 'incoming'}), name='incoming_request'),
]