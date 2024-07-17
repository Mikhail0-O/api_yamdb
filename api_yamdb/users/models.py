from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def validate_role(value):
    if value not in ['user', 'admin', 'moderator']:
        raise ValidationError(f"{value} - недопустимая роль")


class CustomUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=50, blank=True, validators=[validate_role],
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
