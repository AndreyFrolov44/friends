from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers

from .models import RequestFriend
from users.models import User


class RequestSerialiser(serializers.ModelSerializer):
    class Meta:
        model = RequestFriend
        fields = '__all__'


class RequestCreateSerializer(serializers.Serializer):
    to_username = serializers.CharField()

    
