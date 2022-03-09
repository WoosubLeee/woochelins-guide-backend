from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer
from places.serializers import GroupPlaceSerializer


class GroupSerializer(serializers.ModelSerializer):
    places = GroupPlaceSerializer(read_only=True, many=True)
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'places', 'created_at', 'members', 'admins',)


class GroupInvitationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvitationToken
        fields = '__all__'