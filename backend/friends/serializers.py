from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers

from users.serializers import UserSerializer
from .models import RequestFriend


class RequestOutgoingSerialiser(serializers.ModelSerializer):
    to_user = UserSerializer()

    class Meta:
        model = RequestFriend
        fields = ('id', 'to_user', 'is_canceled')

class RequestIncomingSerialiser(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        model = RequestFriend
        fields = ('id', 'from_user', 'is_canceled')


class RequestSentSerializer(serializers.Serializer):
    username = serializers.CharField()

    
