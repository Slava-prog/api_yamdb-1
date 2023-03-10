from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_YAMDB


def send_confirmation_code(email, confirmation_code):
    send_mail(
        'Код подтверждения на YamDB',
        f'Для подтверждения регистрации используйте код:'
        f'{confirmation_code}',
        EMAIL_YAMDB,
        recipient_list=(email,),
        fail_silently=False
    )


def check_confirmation_code(user, confirmation_code):
    return str(user.confirmation_code) == confirmation_code
