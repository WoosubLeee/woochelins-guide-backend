from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.CustomAuthToken.as_view()),
    path('validate/', views.is_valid),
    path('groups-lists/', views.get_user_groups_lists),
]