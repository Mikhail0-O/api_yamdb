from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .mixins import GetTitleMixin, GetReviewMixin
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from .serializers import (CategoriesSerializer,
                          CommentsSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          ReviewsSerializer)
from .permissions import IsAdminOrReadOnly, IsAdminAuthorModeratorOrReadOnly


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'genre', 'category')
    permission_classes = [IsAdminOrReadOnly]


class ReviewsViewSet(GetTitleMixin, viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]

    def perform_create(self, serializer):
        author = self.request.user
        if Reviews.objects.filter(
            title=self.get_title(), author=author
        ).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв!')
        serializer.save(author=author)


class CommentsViewSet(GetReviewMixin, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]

    def get_queryset(self):
        return Comments.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
