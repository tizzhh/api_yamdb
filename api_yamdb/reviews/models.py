from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from custom_user.models import CustomUser
from .constants import (NAME_MAX_LENGTH, SLUG_MAX_LENGTH,
                        OBJECT_NAME_DISPLAY_LENGTH)


class CategoryGenreAbstract(models.Model):
    name = models.CharField('Наименование', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', unique=True, max_length=SLUG_MAX_LENGTH)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:OBJECT_NAME_DISPLAY_LENGTH]


class Title(models.Model):
    name = models.CharField('Наименование', max_length=NAME_MAX_LENGTH)
    year = models.PositiveSmallIntegerField('Год публикации')
    description = models.TextField('Описание', blank=True, default='')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )
    genre = models.ManyToManyField('Genre', verbose_name='Жанры')

    class Meta:
        default_related_name = 'titles'
        ordering = ('name', 'year', 'category')

    def validate(self) -> None:
        current_year = timezone.now().year
        if self.year > current_year:
            raise ValidationError({'year': 'Год публикации не может быть'
                                   'больше текущего'})

    def __str__(self):
        return self.name[:OBJECT_NAME_DISPLAY_LENGTH]


class Category(CategoryGenreAbstract):
    pass


class Genre(CategoryGenreAbstract):
    pass


class Review(models.Model):
    """Model describes parameters of review on title."""

    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Оценка не может быть ниже 1.'),
            MaxValueValidator(10, 'Оценка не может быть выше 10.'),
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    class Meta:
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:]


class Comment(models.Model):
    """Model describes objects of comments to review."""

    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации комментария'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв'
    )

    class Meta:
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
