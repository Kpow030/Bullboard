from django.http import  HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import loginRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import *

@permission_required('polls.add_choice', raise_exception= True)
@login_required
def my_view(request):
    return HttpResponse(content={'count': count_var})


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'


class AdvertCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('bull_board.add_advert',)
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = AdvertForm
    # модель товаров
    model = Advert
    # и новый шаблон, в котором используется форма.
    template_name = 'advert_create.html'
    context_object_name = 'create'


class AdvertUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('bull_board.update_advert',)
    form_class = AdvertForm
    model = Advert
    template_name = 'advert_edit.html'


class AdvertDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('bull_board.delete_post',)
    model = Advert
    template_name = 'advert_delete.html'
    success_url = reverse_lazy('advert_list')