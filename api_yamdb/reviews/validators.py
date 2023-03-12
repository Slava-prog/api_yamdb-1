import datetime

from django.core.exceptions import ValidationError


def my_year_validator(value):
    if value < 0 or value > datetime.datetime.now().year:
        raise ValidationError(
            ('%(value)s - некорректный год!'),
            params={'value': value},
        )


def my_score_validator(value):
    if value < 0 or value > 10:
        raise ValidationError(
            ('Значение должно находиться в диапазоне [0:10]'),
            params={'value': value},
        )
