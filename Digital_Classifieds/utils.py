from django.core.mail import send_mail
from django.conf import settings


def conf_mail(user):
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения регистрации: {user.confirmation_code}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])