# Generated by Django 3.2 on 2024-07-21 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отзыва'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.titles', verbose_name='Произведение'),
        ),
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
        ),
        migrations.AddField(
            model_name='comments',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.reviews', verbose_name='Отзыв'),
        ),
    ]
