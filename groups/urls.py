from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'', views.GroupViewSet)

urlpatterns = [
    path('<int:pk>/invitation/', views.create_token),
    path('<int:pk>/invitation/<str:token>/', views.validate_invitation),
    path('', include(router.urls)),
]
