from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import RequestCreateSerializer
from .models import RequestFriend
from .services import RequestFriendServise
from users.models import User


class RequestViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:   
        serializer = RequestCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        to_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['to_username'])

        return RequestFriendServise.create(from_user=request.user, to_user=to_user)
