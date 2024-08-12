from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, View
from django_filters import FilterSet
from django.db.models import Q

from .forms import ArticleForm, CommentForm, Registration
from .models import *


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
        return redirect('account_login')


class ProfileView(TemplateView):
    template_name = 'profile.html'


class ArticleFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ['post']

    def __init__(self, *args, **kwargs):
        super(ArticleFilter, self).__init__(*args, **kwargs)
        self.filters['commentPost'].queryset = Article.objects.filter(author__id=self.request.user.id)


class IndexView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'profile.html'
    context_object_name = 'comments'
    filterset_class = ArticleFilter

    def get_queryset(self):
        queryset = Comment.objects.filter(commentPost__author__id=self.request.user.id)
        return queryset


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def article_list(request):
        articles = Article.objects.all()
        return render(request, 'article_list.html', {'articles': articles})

    def article_search(request):
        query = request.GET.get('q')
        articles = Article.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
        return render(request, 'article_list.html', {'articles': articles})


class CommentCreate(LoginRequiredMixin, CreateView):
    permission_required = ('Digital_Classfieds.add_comment',)
    raise_exception = True
    model = Comment
    template_name = 'article_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commentUser = self.request.user
        comment.commentPost_id = self.kwargs['pk']
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_id'] = self.kwargs['pk']
        return context


class CommentUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('Digital_Classfieds.change_comment',)
    raise_exception = True
    form_class = CommentForm
    model = Comment
    template_name = 'comment_update.html'

    def get_success_url(self):
        return reverse('article_list')


class CommentDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('Digital_Classfieds.delete_comment',)
    raise_exception = True
    model = Comment
    template_name = 'comment_delete.html'

    def get_success_url(self):
        return reverse('article_list')


class ArticleDetail(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'


class ArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('Digital_Classfieds.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        return super().form_valid(form)


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'

    def get_success_url(self):
        return reverse('article_list')


class RegistrationCreate(CreateView):
    form_class = Registration
    template_name ='register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')


class ResponseView(DetailView):
    model = Article
    template_name ='responses.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = self.object.get_responses()
        return context


class CommentView(DetailView):
    model = Article
    template_name = 'comments.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.get_comments()
        return context


class CommentLikeView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.like()
        return redirect('comments', pk=comment.post.pk)


class CommentDislikeView(View):
    def get(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.dislike()
        return redirect('comments', pk=comment.post.pk)


@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'article_create.html', {'form': form})