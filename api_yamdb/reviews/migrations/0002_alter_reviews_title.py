# Generated by Django 3.2 on 2024-07-21 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='title',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.titles', verbose_name='Произведение'),
        ),
    ]