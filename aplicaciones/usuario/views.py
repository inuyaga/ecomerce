from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.usuario.forms import UserForm, UserFormEdit
from aplicaciones.usuario.models import User
from django.contrib.auth.admin import UserAdmin
from django.views.generic import CreateView, ListView, UpdateView
# Create your views here.

class CreateUser(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserAdmin
    form_class = UserForm
    template_name = 'admin/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:list_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class UsuarioList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'admin/list_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class UsuarioUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = UserFormEdit
    template_name = 'admin/crear_usuarios.html'
    success_url = reverse_lazy('usuarios:list_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context



