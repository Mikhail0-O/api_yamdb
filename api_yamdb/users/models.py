# модель пользователя
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    title = models.CharField(
        'Название', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):

    bio = models.TextField('Биография', blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
