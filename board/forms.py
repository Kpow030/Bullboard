from string import hexdigits
import random

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import TextInput, Textarea
from django.conf import settings
from allauth.account.forms import SignupForm

from .models import Article, Comment


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class ArticleForm(forms.ModelForm):
    text = forms.Textarea()

    class Meta:
        model = Article
        fields = [
            'upload',
            'title',
            'text',
            'author',
            'category',
        ]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы"
            )
        return title

    def clean_text(self):
        text = self.cleaned_data["text"]
        if text[0].islower():
            raise ValidationError(
                "Описание должно начинаться с заглавной буквы"
            )
        return text

    class Meta:
        model = Article
        fields = ['upload', 'title', 'text', 'category']

        widgets = {
            'upload': TextInput(attrs={'class': 'form-control', 'placeholder': 'Загрузите файл'}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок объявления'}),
            'text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание объявления'}),
            'category_': TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'Введите текст отклика:'
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-text', 'cols': 150, 'rows': 1}),
        }


class Registration(forms.ModelForm):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')