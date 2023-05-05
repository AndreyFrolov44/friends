from django.urls import path

from .views import RequestViewSet


urlpatterns = [
    path('', RequestViewSet.as_view({
        'post': 'create'
    })),
]