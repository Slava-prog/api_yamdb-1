from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# from datetime import datetime

from users.models import CustomUser


class Category(models.Model):
    """Класс категорий произведений."""
    name = models.TextField(
        'Категория',
        max_length=200,
        db_index=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории',
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс жанров произведений"""
    name = models.TextField(
        'Жанр',
        max_length=100,
        db_index=True
    )
    slug = models.SlugField(
        'Slug',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры',
        ordering = ['name', ]


class Title(models.Model):
    """Класс произведений, к которым пишут отзыв."""

    name = models.CharField(
        'Название произведения',
        max_length=200,
        db_index=True,
        help_text='Введите название произведения'
    )
    year = models.PositiveIntegerField(
        'Год издания',
        validators=[
            MinValueValidator(
                0, message='Введённое значение не может быть отрицательным'
            ),
            MaxValueValidator(
                2023,
                message='Введённое значение не может быть больше текущего года'
            ),
        ],
        db_index=True,
        help_text='Введите возможный год издания произведения',
    )
    description = models.TextField(
        'Описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения',
        ordering = ['-year', 'name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Класс отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                0, message='Значение должно находиться в диапазоне [0:10]'
            ),
            MaxValueValidator(
                10, message='Значение должно находиться в диапазоне [0:10]'
            ),
        ],
        db_index=True,
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    """Комментарии к отзывам."""
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
