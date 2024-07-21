from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator

from .validators import validate_role, validate_username


class CustomUser(AbstractUser):
    username = models.CharField(
        'username', max_length=150, unique=True,
        validators=[validate_username,
                    MinLengthValidator(limit_value=5),
                    RegexValidator(regex=r'^[\w.@+-]+\Z')]
    )
    email = models.EmailField(
        'email',
        unique=True, max_length=254)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=50, blank=True, validators=[validate_role],
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
