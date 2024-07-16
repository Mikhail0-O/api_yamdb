from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
