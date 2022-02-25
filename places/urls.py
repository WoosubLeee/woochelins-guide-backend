from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'list', views.PlaceListViewSet)
router.register(r'group/list', views.GroupPlaceListViewSet)
router.register(r'', views.PlaceViewSet)

urlpatterns = [
    path('list/user/default/', views.get_user_default_list),
    path('group/list/<int:pk>/<str:google_maps_id>/', views.get_group_place_recommended_by),
    path('saved/user/<str:google_maps_id>/', views.get_user_saved_place),
    path('', include(router.urls)),
]
