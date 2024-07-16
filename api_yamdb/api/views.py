from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Genres
from .serializers import (CategoriesSerializer,
                          GenresSerializer)


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = ('гость сморит всех. удалить и добавить - админ',)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = ('гость сморит всех. удалить и добавить - админ',)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
