from rest_framework import serializers
from .models import *
from places.models import GroupPlaceList
from places.serializers import GroupPlaceListSerializer
from accounts.serializers import UserForGroupSerializer


class GroupSerializer(serializers.ModelSerializer):
    place_list = GroupPlaceListSerializer(read_only=True)
    members = UserForGroupSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'place_list', 'created_at', 'members', 'admin',)

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        GroupPlaceList.objects.create(group=group)
        return group


class GroupInvitationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvitationToken
        fields = '__all__'