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


'''
accounts/groups-placelists 에 사용하는 Serializer
'''
class PlaceListSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = PlaceList
        fields = ('id', 'name',)


class GroupPlaceSerializer(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = GroupPlace
        fields = ('id', 'place', 'place_list', 'recommended_by',)


class GroupPlaceListSerializer(serializers.ModelSerializer):
    places = GroupPlaceSerializer(read_only=True, many=True)

    class Meta:
        model = GroupPlaceList
        fields = ('group', 'places',)
