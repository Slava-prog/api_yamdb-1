from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value < 0 or value > timezone.now().year:
        raise ValidationError(
            ('%(value)s - некорректный год!'),
            params={'value': value},
        )


def score_validator(value):
    if value < 0 or value > 10:
        raise ValidationError(
            ('Значение должно находиться в диапазоне [0:10]'),
            params={'value': value},
        )
