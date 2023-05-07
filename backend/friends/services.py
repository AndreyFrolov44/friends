import enum
from rest_framework import status
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer
from .models import RequestFriend, Friend
from .serializers import RequestOutgoingSerialiser, RequestIncomingSerialiser


class StatusEnum(enum.Enum):
    none = None
    incoming_request = 'Incoming request'
    outgoing_request = 'Outgoing request'
    friends = 'Friends'



class RequestFriendServise:
    @staticmethod
    def create(from_user: User, to_user: User) -> Response:
        if RequestFriend.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'detail': 'Request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        if from_user.friend.friends.filter(id=to_user.id).exists() or to_user.friend.friends.filter(id=from_user.id).exists():
            return Response({'detail': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)
        
        reverse_request = RequestFriend.objects.filter(from_user=to_user, to_user=from_user)


        if reverse_request.first():
            reverse_request.delete()
            return FriendService.create(user=from_user, new_friend=to_user)

        request = RequestFriend(from_user=from_user, to_user=to_user)
        request.save()
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def accept(current_user: User, from_user: User) -> Response:
        if not RequestFriend.objects.filter(from_user=from_user, to_user=current_user).exists():
            return Response({'detail': 'This user has not sent you a friend request'}, status=status.HTTP_400_BAD_REQUEST)
        
        sent_request = RequestFriend.objects.filter(from_user=from_user, to_user=current_user)
        sent_request.delete()

        return FriendService.create(user=current_user, new_friend=from_user)
    
    @staticmethod
    def reject(current_user: User, from_user: User) -> Response:
        if not RequestFriend.objects.filter(from_user=from_user, to_user=current_user).exists():
            return Response({'detail': 'This user has not sent you a friend request'}, status=status.HTTP_400_BAD_REQUEST)
        
        sent_request = RequestFriend.objects.filter(from_user=from_user, to_user=current_user)
        sent_request.update(is_canceled=True)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)
    
    @staticmethod
    def outgoing(user: User) -> Response:
        serializer = RequestOutgoingSerialiser(RequestFriend.objects.filter(from_user=user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def incoming(user: User) -> Response:
        serializer = RequestIncomingSerialiser(RequestFriend.objects.filter(to_user=user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def status(current_user: User, user: User) -> StatusEnum:
        if RequestFriend.objects.filter(from_user=current_user, to_user=user).exists():
            return StatusEnum.outgoing_request
        elif RequestFriend.objects.filter(from_user=user, to_user=current_user).exists():
            return StatusEnum.incoming_request
        else:
            return StatusEnum.none

    

class FriendService:
    @staticmethod
    def create(user: User, new_friend: User) -> Response:
        if user.friend.friends.filter(id=new_friend.id).exists() or new_friend.friend.friends.filter(id=user.id).exists():
            return Response({'detail': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)
        
        f = Friend.objects.get(user=user)
        f.friends.add(new_friend)

        new_f = Friend.objects.get(user=new_friend)
        new_f.friends.add(user)

        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def get_list(user: User) -> Response:
        serializer = UserSerializer(user.friend.friends.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staticmethod
    def status(current_user: User, user: User) -> StatusEnum:
        if current_user.friend.friends.filter(id=user.id).exists():
            return StatusEnum.friends
        return StatusEnum.none
    
    @staticmethod
    def delete(current_user: User, user: User) -> Response:
        friend = current_user.friend.friends.filter(id=user.id)
        if not friend.exists():
            return Response({'detail': 'You are not friends'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_user.friend.friends.remove(user)
        user.friend.friends.remove(current_user)

        return Response(status=status.HTTP_204_NO_CONTENT)
