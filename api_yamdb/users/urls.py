from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CreateUserViewSet

app_name = 'users'

users_router = routers.DefaultRouter()
# users_router.register(TokenObtainPairView)

urlpatterns = [
    path('signup/', CreateUserViewSet.as_view({'post': 'create'})),
    # path('signup/', include('djoser.urls.jwt')),
]
