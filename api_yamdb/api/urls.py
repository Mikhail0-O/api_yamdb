from rest_framework import routers
from django.urls import include, path

from .views import (CategoryViewSet, GenreViewSet, TitlesViewSet,
                    ReviewsViewSet, CommentViewSet,
                    UserViewSet, UserRegistrationViewSet, get_token)


v1_router = routers.DefaultRouter()
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'auth/signup', UserRegistrationViewSet, basename='auth')

app_name = 'api'

urlpatterns = [
    path('v1/auth/token/', get_token, name='token'),
    path('v1/categories/<slug:slug>/',
         CategoryViewSet.as_view({'delete': 'destroy'}),
         name='category-detail'),
    path('v1/categories/', CategoryViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='categories-list-create'),
    path('v1/genres/<slug:slug>/',
         GenreViewSet.as_view({'delete': 'destroy'}),
         name='genre-detail'),
    path('v1/genres/', GenreViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='genres-list-create'),

    path('v1/', include(v1_router.urls)),
]
