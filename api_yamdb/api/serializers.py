from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import status
import re

from api_yamdb.settings import VALID_USERNAME_CHARECTERS
from users.confirmation_code import get_confirmation_code
from .exceptions import CustomValidation
from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date', 'author')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data

        if Review.objects.filter(
                author=self.context.get('request').user,
                title__id=self.context['view'].kwargs.get('title_id')
        ).exclude(
            id=self.instance.id if self.instance else None
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=256)
    rating = serializers.FloatField(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    reviews = ReviewsSerializer(many=True, read_only=True)
    Comment = CommentSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(
            instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre, many=True).data
        return representation

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description',
            'genre', 'category', 'reviews', 'Comment'
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, value):
        pattern = re.compile(VALID_USERNAME_CHARECTERS)
        if not pattern.match(value):
            raise serializers.ValidationError(
                'Имя пользователя должно содержать только буквы, '
                'цифры, точки, @, + или -'
            )
        if value == 'me':
            raise serializers.ValidationError(
                f'Использовать имя "{value}" в качестве username запрещено'
            )
        return value

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if User.objects.filter(email=email, username=username).exists():
            raise CustomValidation(
                'Пользователь успешно создан',
                username, status_code=status.HTTP_200_OK
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': [f'Пользователь с таким {email} уже существует']}
            )

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': [
                    f'Пользователь с таким username '
                    f'{username} уже существует']}
            )

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CustomValidation(
                'Не существует',
                username, status_code=status.HTTP_404_NOT_FOUND
            )

        if confirmation_code != get_confirmation_code(username):
            raise serializers.ValidationError(
                {'confirmation_code': 'Код подтверждения истек или неверен.'}
            )

        data['user'] = user
        return data
