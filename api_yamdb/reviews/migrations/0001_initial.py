# Generated by Django 3.2 on 2024-03-12 19:08

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=256, verbose_name='Наименование'
                    ),
                ),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=256, verbose_name='Наименование'
                    ),
                ),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=256, verbose_name='Наименование'
                    ),
                ),
                (
                    'year',
                    models.PositiveSmallIntegerField(
                        verbose_name='Год публикации'
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True, default='', verbose_name='Описание'
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='titles',
                        to='reviews.category',
                        verbose_name='Категория',
                    ),
                ),
                (
                    'genre',
                    models.ManyToManyField(
                        related_name='titles',
                        to='reviews.Genre',
                        verbose_name='Жанр',
                    ),
                ),
            ],
            options={
                'ordering': ('name', 'year', 'category'),
                'default_related_name': 'titles',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                (
                    'score',
                    models.PositiveSmallIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(
                                1, 'Оценка не может быть ниже 1.'
                            ),
                            django.core.validators.MaxValueValidator(
                                10, 'Оценка не может быть выше 10.'
                            ),
                        ],
                        verbose_name='Оценка',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Дата публикации отзыва',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Пользователь',
                    ),
                ),
                (
                    'title',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='reviews',
                        to='reviews.title',
                        verbose_name='Произведение',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('-pub_date',),
                'default_related_name': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='Текст комментария')),
                (
                    'pub_date',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Дата публикации комментария',
                    ),
                ),
                (
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Пользователь',
                    ),
                ),
                (
                    'review',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to='reviews.review',
                        verbose_name='Отзыв',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
                'default_related_name': 'comments',
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                fields=('author', 'title'), name='unique_author_title'
            ),
        ),
    ]
