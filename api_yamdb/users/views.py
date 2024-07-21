from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.generics import (RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework import filters

from .serializers import (UserRegistrationSerializer, UserSerializer,
                          UserMeSerializer)
from .get_tokens_for_user import get_tokens_for_user
from .confirmation_code import (generate_confirmation_code,
                                store_confirmation_code,
                                get_confirmation_code)


User = get_user_model()


class UserDeleteViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        username = self.kwargs.get('username')
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            pass

    def delete(self, request, username):
        if request.user.is_superuser or request.user.role == 'admin':
            try:
                user = User.objects.get(username=username)
                user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        if request.user.role == 'user' or request.user.role == 'moderator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.is_superuser or request.user.role == 'admin':
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserMeRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username',)

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.role == 'admin':
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def get_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    if username is None or confirmation_code is None:
        return Response(
            {'detail': 'Некоректные данные.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = User.objects.filter(username=username).first()
    if user is None:
        return Response(
            {'detail': f'Пользователь {username} - не существует.'},
            status=status.HTTP_404_NOT_FOUND
        )
    if confirmation_code == get_confirmation_code(username):
        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
    return Response(
        {'detail': f'Код подтверждения {confirmation_code} - истек.'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CreateUserViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')

        missing_fields = {}
        if email is None:
            missing_fields['email'] = ['Отсутствет обязательное поле']
        if username is None:
            missing_fields['username'] = ['Отсутствует обязательное поле']

        if missing_fields:
            return Response(
                missing_fields,
                status=status.HTTP_400_BAD_REQUEST
            )
        user_exists = User.objects.filter(
            email=email, username=username
        ).exists()
        email_exists = User.objects.filter(
            email=email
        ).exists()
        if user_exists:
            headers = self.get_success_headers(request.data)
            return Response(request.data, status=status.HTTP_200_OK)
        if email_exists:
            headers = self.get_success_headers(request.data)
            return Response(
                {'email': f'Полльзователь с таким {email} - уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        confirmation_code = generate_confirmation_code()
        store_confirmation_code(username, confirmation_code)
        send_mail(
            subject='Код подтверждения',
            message=confirmation_code,
            from_email='from@example.com',
            recipient_list=[request.data['email'],],
            fail_silently=True,
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )
