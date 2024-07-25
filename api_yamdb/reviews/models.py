from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import CustomUser
from api.validators import year_validator


class NameModel(models.Model):
    name = models.CharField('Название', max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SlugModel(models.Model):
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    class Meta:
        abstract = True


class TextAuthorPubDate(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True


class Category(NameModel, SlugModel):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Genre(NameModel, SlugModel):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id']


class Title(NameModel):
    year = models.IntegerField('Год выхода', validators=[year_validator])
    description = models.TextField('Описание произведения', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['id']


class Review(TextAuthorPubDate):
    score = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(
                settings.MIN_SCORE_VALUE, message='Минимальная оценка 1'
            ),
            MaxValueValidator(
                settings.MAX_SCORE_VALUE, message='Максимальная оценка 10'
            )
        ]
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            ),
        ]
        ordering = ['-pub_date']

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'


class Comment(TextAuthorPubDate):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Комментарий к отзыву {self.review} от {self.author}'
