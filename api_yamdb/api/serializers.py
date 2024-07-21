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
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Reviews
        fields = (
            'id', 'text', 'rating', 'author', 'title', 'pub_date'
        )

    # def validate(self, data):
    #     request = self.context.get('request')
    #     title = data.get('title')
    #     author = request.user

    #     # Проверяем, существует ли уже отзыв от этого пользователя на это произведение
    #     if Reviews.objects.filter(title=title, author=author).exists():
    #         raise serializers.ValidationError(
    #             'Вы уже оставили отзыв на это произведение.'
    #         )

    #     return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'review', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategoriesSerializer(
            instance.category).data
        representation['genre'] = GenresSerializer(
            instance.genre, many=True).data
        return representation

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category', 'reviews', 'comments'
        )
