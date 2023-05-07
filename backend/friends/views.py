from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .serializers import RequestIncomingSerialiser, RequestOutgoingSerialiser, UsernameSerializer
from .services import RequestFriendServise, FriendService
from users.serializers import UserSerializer
from users.models import User


class RequestViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=UsernameSerializer,
        description='Send a friend request',
        responses={
            201: OpenApiResponse(description='Request has been sent'),
            400: OpenApiResponse(description='Your request has already been sent or you are already a friend'),
            404: OpenApiResponse(description='User does not exist')
        },
    )
    def create(self, request: Request) -> Response:   
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.create(from_user=request.user, to_user=to_user)
    
    @extend_schema(
        request=UsernameSerializer,
        description='Accept friend request',
        responses={
            201: OpenApiResponse(description='Friend request accepted'),
            400: OpenApiResponse(description='This user has not sent you a friend request'),
            404: OpenApiResponse(description='User does not exist')
        },
    )
    def accept(self, request: Request) -> Response:   
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.accept(current_user=request.user, from_user=from_user)

    @extend_schema(
        request=UsernameSerializer,
        description='Reject friend request',
        responses={
            201: OpenApiResponse(description='Friend request rejected'),
            400: OpenApiResponse(description='This user has not sent you a friend request'),
            404: OpenApiResponse(description='User does not exist')
        },
    )
    def reject(self, request: Request) -> Response:   
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return RequestFriendServise.reject(current_user=request.user, from_user=from_user)
    
    @extend_schema(
        description='Outgoing friend requests',
        responses={
            200: RequestOutgoingSerialiser(many=True),
        },
    )
    def outgoing(self, request: Request) -> Response:
        return RequestFriendServise.outgoing(user=request.user)
    
    @extend_schema(
        description='Incoming friend requests',
        responses={
            200: RequestIncomingSerialiser(many=True),
        },
    )
    def incoming(self, request: Request) -> Response:
        return RequestFriendServise.incoming(user=request.user)
    

class FriendViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Get a list of friends',
        responses={
            200: UserSerializer(many=True),
        },
    )
    def get_list(self, request: Request) -> Response:
        return FriendService.get_list(user=request.user)
    
    @extend_schema(
        request=UsernameSerializer,
        description='Delete friend',
        responses={
            204: None,
            400: OpenApiResponse(description='You are not friends'),
            404: OpenApiResponse(description='User does not exist')
        },
    )    
    def delete(self, request: Request) -> Response:
        serializer = UsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

        return FriendService.delete(current_user=request.user, user=user)
    

@extend_schema(
    parameters=[OpenApiParameter(name='username', required=True, type=str)],
    description='Get friend status',
    responses={
        200: OpenApiResponse(description='Null, Incoming request, Outgoing request or Friends'),
        404: OpenApiResponse(description='User does not exist')
    },
) 
@api_view()
def get_status(request: Request) -> Response:
    serializer = UsernameSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(User, ~Q(id=request.user.id), username=serializer.data['username'])

    friend_status = FriendService.status(current_user=request.user, user=user)

    if friend_status.value is not None:
        return Response({'status': friend_status.value}, status=status.HTTP_200_OK)
    return Response({'status': RequestFriendServise.status(current_user=request.user, user=user).value}, status=status.HTTP_200_OK)
