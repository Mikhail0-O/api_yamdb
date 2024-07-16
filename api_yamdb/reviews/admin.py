from django.contrib import admin

from .models import Categories, Genres, Titles


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
    )
    search_fields = ('name', 'year', 'rating', 'genre', 'category')


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Categories)
