from django.db import models
from djando.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


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
                datetime.now().year(),
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
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения',
        ordering = ['-year', 'name']

    def __str__(self):
        return self.name
