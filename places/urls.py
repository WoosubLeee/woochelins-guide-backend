from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'list', views.PlaceListViewSet)
router.register(r'group/list', views.GroupPlaceListViewSet)

urlpatterns = [
    path('list/user/default/', views.get_user_default_list),
    path('', include(router.urls)),
]
