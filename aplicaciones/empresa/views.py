from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.empresa.models import Zona, Sucursal
from aplicaciones.empresa.forms import ZonaForm, SucursalForm
from django.urls import reverse_lazy
from aplicaciones.empresa.eliminaciones import get_deleted_objects
# Create your views here.

class inicio(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'admin/base_ecomer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class ZonaCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Zona
    template_name = 'ecomer/crear_zona.html'
    form_class = ZonaForm
    success_url = reverse_lazy('empresa:list_zona')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class ZonaList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Zona
    template_name = 'ecomer/zonalist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class ZonaUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Zona
    template_name = 'ecomer/crear_zona.html'
    form_class = ZonaForm
    success_url = reverse_lazy('empresa:list_zona')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context


class ZonaDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Zona
    template_name = 'eliminaciones.html'
    success_url = reverse_lazy('empresa:list_zona')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class SucursalList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    template_name = 'ecomer/sucursales_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class SucursalCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    template_name = 'ecomer/crear_suc.html'
    form_class = SucursalForm
    success_url = reverse_lazy('empresa:list_sucursales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class SucursalUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    template_name = 'ecomer/crear_suc.html'
    form_class = SucursalForm
    success_url = reverse_lazy('empresa:list_sucursales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context


class SucursalDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    template_name = 'eliminaciones.html'
    success_url = reverse_lazy('empresa:list_sucursales')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context







