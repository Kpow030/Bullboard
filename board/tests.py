from django.core import mail
from django.test import TestCase
from django.core.mail import send_mail

from .models import Article


class EmailTest(TestCase):
    def test_send_email(self):
        subject = 'Тестовое сообщение'
        message = 'Это тестовое сообщение'
        from_email = 'ваш_email@gmail.com'
        to_email = 'адрес_получателя@gmail.com'

        send_mail(subject, message, from_email, [to_email])

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, message)


class ArticleTest(TestCase):
    def test_article(self):
        article = Article.objects.create(title='Проведем тест статьи', text='Это статься написана для теста')
        self.assertEqual(article.title, 'Тест')
        self.assertEqual(article.text, 'Тест2')