from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .models import UserResponse


@receiver(pre_save, sender=User)
def my_handler(sender, instanse, created, **kwargs):
    if instanse.status:
        return
    mail = instanse.autor.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False
    )


    mail = instanse.article.autor.email
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False
    )
