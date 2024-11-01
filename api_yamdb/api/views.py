from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_yamdb.settings import ADMIN_EMAIL
from .filters import TitlesFilter
from .mixins import (GetTitleMixin, GetReviewMixin, UpdateMethodMixin,
                     IsAdminAuthorModeratorOrReadOnlyMixin,
                     IsAdminOrReadOnlyMixin, SearchFilterMixin)
from .permissions import IsAdmin
from reviews.models import Category, Comment, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TitlesSerializer,
                          ReviewsSerializer, UserRegistrationSerializer,
                          UserSerializer, UserMeSerializer, TokenSerializer)
from users.get_tokens_for_user import get_tokens_for_user
from users.confirmation_code import (generate_confirmation_code,
                                     store_confirmation_code)


User = get_user_model()


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      IsAdminOrReadOnlyMixin,
                      SearchFilterMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   IsAdminOrReadOnlyMixin,
                   SearchFilterMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs.get('slug'))

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(UpdateMethodMixin, IsAdminOrReadOnlyMixin,
                    viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'year', 'genre__name', 'category__name')
    filterset_class = TitlesFilter


class ReviewsViewSet(GetTitleMixin, UpdateMethodMixin,
                     IsAdminAuthorModeratorOrReadOnlyMixin,
                     viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(GetReviewMixin, UpdateMethodMixin,
                     IsAdminAuthorModeratorOrReadOnlyMixin,
                     viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class UserRegistrationViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_confirmation_email(user.username, user.email)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response

    def send_confirmation_email(self, username, email):
        confirmation_code = generate_confirmation_code()
        store_confirmation_code(username, confirmation_code)
        send_mail(
            subject='Код подтверждения',
            message=confirmation_code,
            from_email=ADMIN_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )


class UserViewSet(UpdateMethodMixin, SearchFilterMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('^username',)
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    user = User.objects.filter(
        username=serializer.validated_data.get('username')
    ).first()
    tokens = get_tokens_for_user(user)
    return Response(tokens, status=status.HTTP_200_OK)
