from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import RequestSentSerializer
from .services import RequestFriendServise
from users.models import User


class RequestViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:   
        serializer = RequestSentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.create(from_user=request.user, to_user=to_user)
    
    def accept(self, request: Request) -> Response:   
        serializer = RequestSentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.accept(current_user=request.user, from_user=from_user)

    def reject(self, request: Request) -> Response:   
        serializer = RequestSentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.reject(current_user=request.user, from_user=from_user)
    
    def outgoing(self, request: Request) -> Response:
        return RequestFriendServise.outgoing(user=request.user)
    
    def incoming(self, request: Request) -> Response:
        return RequestFriendServise.incoming(user=request.user)
