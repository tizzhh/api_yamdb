from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from . import constants
from .validators import validate_year

YamdbUser = get_user_model()


class CategoryGenreAbstract(models.Model):
    name = models.CharField(
        'Наименование', max_length=constants.NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        'Слаг', unique=True, max_length=constants.SLUG_MAX_LENGTH
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[: constants.OBJECT_NAME_DISPLAY_LENGTH]


class Title(models.Model):
    name = models.CharField(
        'Наименование', max_length=constants.NAME_MAX_LENGTH
    )
    year = models.SmallIntegerField(
        'Год публикации', validators=[validate_year]
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
    )
    genre = models.ManyToManyField('Genre', verbose_name='Жанр')

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[: constants.OBJECT_NAME_DISPLAY_LENGTH]


class Category(CategoryGenreAbstract):
    class Meta(CategoryGenreAbstract.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreAbstract):
    class Meta(CategoryGenreAbstract.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Review(models.Model):
    """Model describes parameters of review on title."""

    text = models.TextField('Текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        YamdbUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                constants.MIN_SCORE_VALUE, 'Оценка не может быть ниже 1.'
            ),
            MaxValueValidator(
                constants.MAX_SCORE_VALUE, 'Оценка не может быть выше 10.'
            ),
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
        return self.text[: constants.OBJECT_NAME_DISPLAY_LENGTH]


class Comment(models.Model):
    """Model describes objects of comments to review."""

    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE, verbose_name='Пользователь'
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
        return self.text[: constants.OBJECT_NAME_DISPLAY_LENGTH]
