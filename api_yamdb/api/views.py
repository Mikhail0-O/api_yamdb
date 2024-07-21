from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status

from .mixins import GetTitleMixin, GetReviewMixin
from reviews.models import Categories, Comments, Genres, Reviews, Titles
from .serializers import (CategoriesSerializer,
                          CommentsSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          ReviewsSerializer)
from .permissions import IsAdminOrReadOnly, IsAdminAuthorModeratorOrReadOnly
from .filters import TitlesFilter


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

    def get_object(self):
        return get_object_or_404(Categories, slug=self.kwargs.get('slug'))

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenresViewSet(mixins.ListModelMixin,
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

    def get_object(self):
        return get_object_or_404(Genres, slug=self.kwargs.get('slug'))

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'year', 'genre__name', 'category__name')
    filterset_class = TitlesFilter

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


class ReviewsViewSet(GetTitleMixin, viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]

    # def create(self, request, *args, **kwargs):
    #     author = request.user
    #     title = self.get_title()

    #     # Проверяем, существует ли уже отзыв от этого пользователя на это произведение
    #     if Reviews.objects.filter(title=title, author=author).exists():
    #         return Response(
    #             {'detail': 'Вы уже оставили отзыв на это произведение!'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # Если нет, вызываем метод create родительского класса
    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        author = self.request.user
        if Reviews.objects.filter(
            title=self.get_title(), author=author
        ).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв!')
        serializer.save(author=author)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)


class CommentsViewSet(GetReviewMixin, viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]

    def get_queryset(self):
        return Comments.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT')
        return super().update(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
