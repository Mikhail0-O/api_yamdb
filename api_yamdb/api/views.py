from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories
from .serializers import CategoriesSerializer


class CategoriesViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.obgects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = ('гость сморит всех. удалить и добавить - админ',)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
