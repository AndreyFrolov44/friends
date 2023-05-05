from rest_framework import status
from rest_framework.response import Response

from users.models import User
from .models import RequestFriend


class RequestFriendServise:
    @staticmethod
    def create(from_user: User, to_user: User) -> Response:
        if RequestFriend.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"detail": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        
        if RequestFriend.objects.filter(from_user=to_user, to_user=from_user).exists():
            return Response({"status": "TODO"}, status=status.HTTP_201_CREATED)

        request = RequestFriend(from_user=from_user, to_user=to_user)
        request.save()
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)