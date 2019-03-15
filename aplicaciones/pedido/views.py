from django.shortcuts import render
from django.views.generic import CreateView,ListView,UpdateView,DeleteView
from aplicaciones.pedido.models import *
from aplicaciones.pedido.forms import *
from django.urls import reverse_lazy
from aplicaciones.empresa.eliminaciones import get_deleted_objects
class ProductoLista(ListView):
    model=Producto
    template_name='pedido/productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class PrductoCreate(CreateView) :
    model = Producto
    form_class = ProductoForm
    template_name = 'pedido/crear_producto.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
class ProductoUpdate(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'pedido/crear_producto.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class ProductoDelete(DeleteView):
    model = Producto
    template_name = 'eliminaciones.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class PedidoList(ListView):
    model=Pedido
    template_name = 'pedido/pedido_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
    def get_queryset(self):
        queryset = super(PedidoList, self).get_queryset()
        self.request.user
        if self.request.user.is_superuser:
            pass
        elif self.request.user.tipo_user == 1:
            id_zona=self.request.user.zona_pertene
            queryset=queryset.filter(ped_id_Suc__suc_zona=id_zona)
            print('soy supervisor')
        elif self.request.user.tipo_user == 2:
            pass

        return queryset

