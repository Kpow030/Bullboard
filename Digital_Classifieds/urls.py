"""
URL configuration for Bullboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from bull_board.views import ArticleList, ProfileView, ArticleCreate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('article/', ArticleList.as_view(), name='ArticleList'),
    path('article/<str:page>/', ArticleList.as_view(), name='ArticleListPage'),
    path('accounts/', include('allauth.urls')),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('home/', TemplateView.as_view(template_name='default.html')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('logout/', LogoutView.as_view()),
    path('create/', ArticleCreate.as_view(), name='ArticleCreate'),
    path('create/<str:page>/', ArticleCreate.as_view(), name='ArticleCreatePage')
] + static(settings.MEDIA_URL, document_poot=settings.MEDIA_ROOT)
