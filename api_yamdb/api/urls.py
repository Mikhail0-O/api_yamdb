from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from users.views import UserViewSet, UserMeRetrieveUpdate, UserDeleteViewSet


router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register('users', UserViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', UserMeRetrieveUpdate.as_view()),
    path('v1/users/<str:username>/', UserDeleteViewSet.as_view(), name='user-delete'),
    path('v1/', include(router.urls)),
]
