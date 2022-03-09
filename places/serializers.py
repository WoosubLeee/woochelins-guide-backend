from rest_framework import serializers
from .models import *
from accounts.serializers import UserSerializer


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class GroupPlaceSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    recommenders = UserSerializer(read_only=True, many=True)

    class Meta:
        model = GroupPlace
        fields = ('id', 'place', 'group', 'recommenders',)


class MyListSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(read_only=True, many=True)

    class Meta:
        model = MyList
        fields = ('id', 'name', 'user', 'is_default', 'places',)