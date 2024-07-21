from django.contrib import admin
from django.db.models import Avg

from .models import Categories, Comments, Genres, Titles, Reviews


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'description', 'category',
        'average_rating', 'genres'
    )
    search_fields = ('name', 'year', 'category__name')
    list_filter = ('year', 'category', 'genre')
    list_editable = ('year', 'category')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(average_rating=Avg('reviews__score'))
        return queryset

    def average_rating(self, obj):
        return (
            round(obj.average_rating, 2)
            if obj.average_rating is not None
            else 0
        )

    average_rating.short_description = 'Average Rating'
    average_rating.admin_order_field = 'average_rating'

    def genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    genres.short_description = 'Genres'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review', 'pub_date')
    search_fields = ('id', 'author__username', 'review__text', 'pub_date')
    list_filter = ('pub_date', 'author')
    list_editable = ('text',)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'title', 'pub_date')
    search_fields = ('id', 'text', 'score', 'pub_date', 'title__name')
    list_filter = ('pub_date', 'score', 'author')
    list_editable = ('score', 'text')


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Reviews, ReviewsAdmin)
