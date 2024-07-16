from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
