import django_filters

from reviews.models import Titles


class TitlesFilter(django_filters.FilterSet):
    genre = django_filters.AllValuesMultipleFilter(field_name='genre__slug')
    category = django_filters.AllValuesFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name',
                                     lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = {
            'genre': ['exact'],
            'category': ['exact'],
            'year': ['exact'],
            'name': ['icontains'],
        }
