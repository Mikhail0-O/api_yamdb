from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Categories, Comments, Genres, Review, Title


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
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')  # Удалите 'title' из полей
        read_only_fields = ('pub_date', 'author')  # Сделайте 'pub_date' и 'author' только для чтения

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(
                author=user,
                title__id=title_id
        ).exclude(
            id=self.instance.id if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data


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
            return reviews.aggregate(Avg('score'))['score__avg']
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategoriesSerializer(
            instance.category).data
        representation['genre'] = GenresSerializer(
            instance.genre, many=True).data
        return representation

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category', 'reviews', 'comments'
        )
