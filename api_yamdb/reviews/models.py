import datetime as dt

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, Q


User = get_user_model()


class Title(models.Model):
    name = models.CharField('Наименование', max_length=256)
    year = models.IntegerField('Год публикации')
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 verbose_name='Категория', null=True)
    genre = models.ManyToManyField('Genre', verbose_name='Жанры')

    class Meta:
        default_related_name = 'titles'
        ordering = ['name', 'year', 'category']

        constraints = [
            CheckConstraint(
                check=Q(year__lte=dt.datetime.now().year),
                name='Год выпуска не может быть больше текущего'
            )
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
