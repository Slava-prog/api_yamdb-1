import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR)
]


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Никнейм'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта'
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4(),
        verbose_name='Код'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
