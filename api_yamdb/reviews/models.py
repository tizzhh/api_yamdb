import datetime as dt

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q


User = get_user_model()


class Title(models.Model):
    name = models.CharField('Наименование', max_length=50)
    year = models.IntegerField('Год публикации')
    rating = ...  # Здесь нужно привязать рейтинг видимо с Review моделями...
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='category')
    genre = models.ManyToManyField('Genre', through='Genre_Title',
                                   verbose_name='Жанры',
                                   related_name='genre')

    class Meta:
        ordering = ['name', 'year', 'category']

        constraints = [
            CheckConstraint(
                check=Q(year__gt=dt.datetime.now().year()),
                name='Год выпуска не может быть больше текущего'
            )
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Наименование', max_length=50)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Наименование', max_length=50)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Произведение')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Жанр')

    class Meta:
        ordering = ['title', 'genre']
