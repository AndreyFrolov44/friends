from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UsernameSerializer
from .services import RequestFriendServise, FriendService
from users.models import User


class RequestViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:   
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.create(from_user=request.user, to_user=to_user)
    
    def accept(self, request: Request) -> Response:   
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.accept(current_user=request.user, from_user=from_user)

    def reject(self, request: Request) -> Response:   
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.reject(current_user=request.user, from_user=from_user)
    
    def outgoing(self, request: Request) -> Response:
        return RequestFriendServise.outgoing(user=request.user)
    
    def incoming(self, request: Request) -> Response:
        return RequestFriendServise.incoming(user=request.user)
    

class FriendViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_list(self, request: Request) -> Response:
        return FriendService.get_list(user=request.user)
    

@api_view()
def get_status(request: Request) -> Response:
    serializer = UsernameSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

    friend_status = FriendService.status(current_user=request.user, user=user)

    if friend_status.value is not None:
        return Response({'status': friend_status.value}, status=status.HTTP_200_OK)
    return Response({'status': RequestFriendServise.status(current_user=request.user, user=user).value}, status=status.HTTP_200_OK)
