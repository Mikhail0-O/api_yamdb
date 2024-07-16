from rest_framework import routers

from django.urls import include, path

from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    ReviewsViewSet, CommentsViewSet)


v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('genres', GenresViewSet)
v1_router.register('titles', TitlesViewSet)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
