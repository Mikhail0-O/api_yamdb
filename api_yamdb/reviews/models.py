from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import CustomUser


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


class Reviews(models.Model):
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Рейтинг',
        choices=[(i, i) for i in range(
            settings.MIN_RATING_VALUE, (settings.MAX_RATING_VALUE + 1)
        )],  # Даем выбрать значение
        default=0
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Titles,
        related_name='reviews',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        # unique_together = ('author', 'title')

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'

    # def clean(self):
    #     # Проверка, существует ли уже отзыв этого пользователя на это произведение
    #     if Reviews.objects.filter(
    #             author=self.author,
    #             title=self.title).exclude(id=self.id).exists():
    #         raise ValidationError('Вы уже оставили отзыв на это произведение.')
    #     super().clean()


class Comments(models.Model):
    text = models.TextField('Текст комментария', max_length=500)
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Reviews,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий к отзыву {self.review} от {self.author}'
