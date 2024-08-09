from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Exists
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django_filters import FilterSet


from.filters import CommentFilter
from.forms import ArticleForm, CommentForm
from.models import Article, Subscription, Comment, User


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
    form_class = CommentFilter
    model = Comment
    template_name = 'profile.html'
    context_object_name = 'comments'

    def get_queryset(self):
        queryset = Comment.objects.filter(commentPost__author__id=self.request.user.id)
        self.filterset = ArticleFilter(self.request.GET, queryset, request=self.request)
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 5


class CommentCreate(LoginRequiredMixin, CreateView):
    permission_required = ('testapp.add_comment',)
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
    permission_required = ('testapp.change_comment',)
    raise_exception = True
    form_class = CommentForm
    model = Comment
    template_name = 'comment_update.html'
    success_url = reverse_lazy('article_list')


class CommentDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('testapp.delete_comment',)
    raise_exception = True
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('article_list')


class ArticleDetail(DetailView, CommentCreate):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'


class ArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('testapp.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_create')

    def form_valid(self, form):
        new_article = form.save(commit=False)
        if self.request.method == 'POST':
            new_article.author = self.request.user
        new_article.save()
        return super().form_valid(form)


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


def zone_view(request):
    if request.method == 'POST':
        zone = request.POST.get('zone')
        print(zone)
        return redirect('next_view')
    return render(request, 'zone.html')


