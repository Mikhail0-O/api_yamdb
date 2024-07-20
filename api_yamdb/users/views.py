from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.decorators import api_view

from .serializers import UserRegistrationSerializer, UserSerializer
from .get_tokens_for_user import get_tokens_for_user
from .confitmation_code import (generate_confirmation_code,
                                store_confirmation_code,
                                get_confirmation_code)


User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination


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
        # print(get_tokens_for_user(User.objects.filter(username='Donald').first()).get('access'))
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
            print(get_confirmation_code(username))
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
        print(get_confirmation_code(username))
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
