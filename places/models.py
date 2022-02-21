from operator import mod
from django.db import models
from django.conf import settings
from groups.models import *


User = settings.AUTH_USER_MODEL

class Place(models.Model):
    google_maps_id = models.CharField(primary_key=True, max_length=50, default='')
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=11, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, default=0)


class PlaceList(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='place_lists')
    is_default = models.BooleanField(default=False, blank=True)
    places = models.ManyToManyField(Place, related_name='place_lists', blank=True)


class GroupPlaceList(models.Model):
    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name='place_list',
        primary_key=True
    )


class GroupPlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    place_list = models.ForeignKey(GroupPlaceList, on_delete=models.CASCADE, related_name='places')
    recommended_by = models.ManyToManyField(User, blank=True, related_name='recommended')
