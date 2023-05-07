from django.urls import path

from .views import RequestViewSet, FriendViewSet, get_status


urlpatterns = [
    path('request/', RequestViewSet.as_view({'post': 'create'}), name='sent_request'),
    path('request/accept/', RequestViewSet.as_view({'post': 'accept'}), name='accept_request'),
    path('request/reject/', RequestViewSet.as_view({'post': 'reject'}), name='reject_request'),
    path('request/outgoing/', RequestViewSet.as_view({'get': 'outgoing'}), name='outgoing_request'),
    path('request/incoming/', RequestViewSet.as_view({'get': 'incoming'}), name='incoming_request'),
    path('', FriendViewSet.as_view({'get': 'get_list'}), name='friend_list'),
    path('delete/', FriendViewSet.as_view({'delete': 'delete'}), name='delete'),
    path('status/', get_status, name='status')
]