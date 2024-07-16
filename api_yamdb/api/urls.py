from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
