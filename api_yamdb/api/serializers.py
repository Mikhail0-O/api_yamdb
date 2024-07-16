from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Reviews, Titles


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class ReviewsSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Reviews
        fields = (
            'id', 'text', 'rating', 'author_username', 'title', 'pub_date'
        )


class CommentsSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author_username', 'review', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    reviews = ReviewsSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category', 'reviews', 'comments'
        )