# модель пользователя
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Пользовательская роль', max_length=150, default='user'
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
