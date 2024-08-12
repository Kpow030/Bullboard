from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify


class Article(models.Model):
    ROLE = (
        ('tank', 'Танк (Warrior)'),
        ('heal', 'Хилы (Healer)'),
        ('dd', 'ДД (Damage Dealer)'),
        ('buyers', 'Торговцы (Merchant)'),
        ('gildmaster', 'Гилдмастеры (Guild Leader)'),
        ('quest', 'Квестгиверы (Quest Giver)'),
        ('smith', 'Кузнецы (Blacksmith)'),
        ('tanner', 'Кожевники (Leatherworker)'),
        ('potion', 'Зельевары (Alchemist)'),
        ('spellmaster', 'Мастера заклинаний (Mage)'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор публикации')
    title = models.CharField(max_length=64, verbose_name='Название объявления')
    text = models.TextField(verbose_name='Описание объявления')
    slug = models.SlugField(max_length=200, unique=True)
    category = models.CharField(max_length=16, choices=ROLE, default='tank', verbose_name='Роль')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    upload = RichTextUploadingField(verbose_name='Приложенный файл')
    app_label = 'myboard'

    def __str__(self):
        return f'{self.id} : {self.title}'

    def get_absolute_url(self):
        return f'/article/{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'announcement'
        verbose_name_plural = 'announcements'
        ordering = ['-dateCreation']

    def get_responses(self):
        return UserResponse.objects.filter(article=self)

    def get_comments(self):
        return Comment.objects.filter(post=self)


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class Advert(models.Model):
    heading = models.CharField(max_length=20, unique=True)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()


class Comment(models.Model):
    STATUS = [
        ('unknown', 'under consideration'),
    ]
    post = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    commentArticle = models.ForeignKey(Article, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
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