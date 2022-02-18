from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name='groups', blank=True)
    admin = models.ManyToManyField(User, related_name='group_admins', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
