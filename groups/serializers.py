from rest_framework import serializers
from .models import *
from places.models import GroupPlaceList
from places.serializers import GroupPlaceListSerializer


class GroupSerializer(serializers.ModelSerializer):
    place_list = GroupPlaceListSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'place_list', 'created_at', 'members', 'admin',)

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        GroupPlaceList.objects.create(group=group)
        return group
