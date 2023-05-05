from rest_framework import status
from rest_framework.response import Response

from users.models import User
from .models import RequestFriend, Friend


class RequestFriendServise:
    @staticmethod
    def create(from_user: User, to_user: User) -> Response:
        if RequestFriend.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"detail": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        if from_user.friend.friends.filter(id=to_user.id).exists() or to_user.friend.friends.filter(id=from_user.id).exists():
            return Response({"detail": "You are already friends"}, status=status.HTTP_400_BAD_REQUEST)
        
        reverse_request = RequestFriend.objects.filter(from_user=to_user, to_user=from_user)


        if reverse_request.first():
            reverse_request.delete()
            print(from_user.id)
            print(to_user.id)
            return FriendService.create(user=from_user, new_friend=to_user)

        request = RequestFriend(from_user=from_user, to_user=to_user)
        request.save()
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
    

class FriendService:
    @staticmethod
    def create(user: User, new_friend: User) -> Response:
        if user.friend.friends.filter(id=new_friend.id).exists() or new_friend.friend.friends.filter(id=user.id).exists():
            return Response({"detail": "You are already friends"}, status=status.HTTP_400_BAD_REQUEST)
        
        f = Friend.objects.get(user=user)
        f.friends.add(new_friend)

        new_f = Friend.objects.get(user=new_friend)
        new_f.friends.add(user)

        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)