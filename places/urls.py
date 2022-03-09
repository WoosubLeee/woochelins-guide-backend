from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'place', views.PlaceViewSet)
router.register(r'groupplace', views.GroupPlaceViewSet)
router.register(r'mylist', views.MyListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
