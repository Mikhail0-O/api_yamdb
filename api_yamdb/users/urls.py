from django.urls import path
from rest_framework import routers

# from .views import CreateUserViewSet, get_token
from .views import UserViewSet, get_token

app_name = 'users'

users_router = routers.DefaultRouter()

urlpatterns = [
    # path('signup/', UserViewSet.as_view({'post': 'create'})),
    # path('token/', get_token),
]
