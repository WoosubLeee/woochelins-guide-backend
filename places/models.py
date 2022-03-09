from django.db import models
from django.conf import settings
from groups.models import *


User = settings.AUTH_USER_MODEL


class Place(models.Model):
    kakao_map_id = models.CharField(primary_key=True, max_length=100, default='')
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    kakao_map_url = models.TextField()

    def save(self, *args, **kwargs):
        self.latitude = round(self.latitude, 10)
        self.longitude = round(self.longitude, 10)
        super().save(*args, **kwargs)


class GroupPlace(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='places')
    recommenders = models.ManyToManyField(User, blank=True, related_name='recommendations')


class MyList(models.Model):
    name = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_lists')
    is_default = models.BooleanField(default=False)
    places = models.ManyToManyField(Place, blank=True)