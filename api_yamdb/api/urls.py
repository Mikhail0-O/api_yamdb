from rest_framework import routers
from django.urls import include, path

from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    ReviewsViewSet, CommentsViewSet)
from users.views import UserViewSet, UserMeRetrieveUpdate, UserDeleteViewSet

v1_router = routers.DefaultRouter()
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)
v1_router.register('users', UserViewSet, basename='users')

app_name = 'api'

urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', UserMeRetrieveUpdate.as_view()),
    path(
        'v1/users/<str:username>/',
        UserDeleteViewSet.as_view(), name='user-delete'
    ),
    path('v1/categories/<slug:slug>/',
         CategoriesViewSet.as_view({'delete': 'destroy'}),
         name='category-detail'),
    path('v1/categories/', CategoriesViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='categories-list-create'),
    path('v1/genres/<slug:slug>/',
         GenresViewSet.as_view({'delete': 'destroy'}),
         name='genre-detail'),
    path('v1/genres/', GenresViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='genres-list-create'),

    path('v1/', include(v1_router.urls)),
]
