from django.urls import path, include
from rest_framework import routers

from .views import CreateUserViewSet, get_token

app_name = 'users'

users_router = routers.DefaultRouter()

urlpatterns = [
    path('signup/', CreateUserViewSet.as_view({'post': 'create'})),
    path('token/', get_token),
]
