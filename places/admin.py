from django.contrib import admin
from .models import *

admin.site.register(Place)
admin.site.register(PlaceList)
admin.site.register(GroupPlaceList)
admin.site.register(GroupPlace)