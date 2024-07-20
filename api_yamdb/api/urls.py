from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from users.views import UserViewSet


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register('users', UserViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/', include(router.urls)),
]
