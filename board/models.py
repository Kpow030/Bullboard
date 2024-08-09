from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    TYPE = (
        ('tank', 'Танк'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildmaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=64, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Описание')
    category = models.CharField(max_length=16, choices=TYPE, default='tank', verbose_name='Категория')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    upload = RichTextUploadingField(verbose_name='Загрузка файла')

    def __str__(self):
        return f'{self.id} : {self.title}'

    def get_absolut_url(self):
        return f'/article/{self.pk}'

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'
        ordering = ['-dateCreation']


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class Advert(models.Model):
    heading = models.TextField(max_length=20, unique=True)
    text = models.TextField()
    dateCreations = models.DateTimeField(auto_now_add=True)
    images = models.ImageField()


class Comment(models.Model):
    STATUS = [
        ('unkown', 'на рассмотрении'),

    ]
    post = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    commentArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreations = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    article = models.ForeignKey(
        to='Article',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )