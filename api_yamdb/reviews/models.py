from django.db import models

from django.core.exceptions import ValidationError
from django.utils import timezone


class Categories(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выхода')
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанры',
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

    def clean(self):
        # Проверка, что год выхода не больше текущего года
        if self.year > timezone.now().year:
            raise ValidationError(
                'Год выхода не может быть больше текущего года.'
            )

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)
