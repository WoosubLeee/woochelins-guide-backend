from rest_framework import serializers
from .models import *


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceListSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(read_only=True, many=True)

    class Meta:
        model = PlaceList
        fields = ('id', 'name', 'user', 'is_default', 'places',)


class GroupPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupPlace
        fields = '__all__'


class GroupPlaceListSerializer(serializers.ModelSerializer):
    places = GroupPlaceSerializer(read_only=True, many=True)

    class Meta:
        model = GroupPlaceList
        fields = ('group', 'places',)
