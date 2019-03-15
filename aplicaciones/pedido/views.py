from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from aplicaciones.pedido.models import *
from aplicaciones.pedido.forms import *

class ProductoLista(ListView):
    model=Producto
    form_class= ProductoForm
    template_name='pedido/productos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context