from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.usuario.forms import UserForm, UserFormEdit
from aplicaciones.usuario.models import User
from django.contrib.auth.admin import UserAdmin
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
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

    @method_decorator(permission_required('usuario.add_user',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(CreateUser, self).dispatch(*args, **kwargs)

class UsuarioList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = User
    template_name = 'admin/list_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    @method_decorator(permission_required('usuario.view_user',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(UsuarioList, self).dispatch(*args, **kwargs)

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

    @method_decorator(permission_required('usuario.change_user',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(UsuarioUpdate, self).dispatch(*args, **kwargs)



