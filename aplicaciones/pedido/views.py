from django.shortcuts import render,redirect
from django.views.generic import CreateView,ListView,UpdateView,DeleteView, TemplateView, DetailView
from aplicaciones.pedido.models import *
from aplicaciones.pedido.forms import *
from django.urls import reverse_lazy
from aplicaciones.empresa.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from openpyxl.styles import Font, Fill, Alignment
from django.http import HttpResponse
from openpyxl import Workbook

class ProductoLista(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model=Producto
    paginate_by = 15
    template_name='pedido/productos.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

class PrductoCreate(LoginRequiredMixin, CreateView) :
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Producto
    form_class = ProductoForm
    template_name = 'pedido/crear_producto.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    @method_decorator(permission_required('pedido.add_producto',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
class ProductoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Producto
    form_class = ProductoForm
    template_name = 'pedido/crear_producto.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    @method_decorator(permission_required('pedido.change_producto',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

class ProductoDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
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

    @method_decorator(permission_required('pedido.delete_producto',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

class PedidoList(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model=Pedido
    template_name = 'pedido/pedido_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
    def get_queryset(self):
        queryset = super(PedidoList, self).get_queryset()
        status = self.request.GET.get('status')

        if self.request.user.is_superuser or self.request.user.tipo_user == 2:
            if status != None:
                queryset=queryset.filter(ped_estatusPedido=status)

        elif self.request.user.tipo_user == 1:
            id_zona=self.request.user.zona_pertene
            queryset=queryset.filter(ped_id_Suc__suc_zona=id_zona)
            if status != None:
                queryset=queryset.filter(ped_estatusPedido=status)

        elif self.request.user.tipo_user == 3:
            id_suc=self.request.user.suc_pertene
            queryset=queryset.filter(ped_id_Suc=id_suc)
            if status != None:
                queryset=queryset.filter(ped_estatusPedido=status)

        return queryset

class CarritoLista(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model=DetallePedido
    template_name='pedido/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    def get_queryset(self):
        queryset = super(CarritoLista, self).get_queryset()
        queryset = queryset.filter(dtl_creado_por=self.request.user, dtl_status=False)
        return queryset

    def post(self, request, *args, **kwargs):
        pedido=Pedido(
            ped_id_Suc=self.request.user.suc_pertene,
            ped_id_UsuarioCreo=self.request.user,
        )
        pedido.save()
        DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_status=False).update(dtl_status=True,dtl_id_pedido=pedido)
        return redirect("/")

class CarritoDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model=DetallePedido
    template_name = 'eliminaciones.html'
    success_url=reverse_lazy('pedido:carrito')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        return context

class DowloadExcelPedido(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request , *args, **kwargs):
        from openpyxl.utils import get_column_letter
        wb = Workbook()
        ws=wb.active
        id_pedido=self.kwargs.get('pk')
        ped = Pedido.objects.get(ped_id_ped=id_pedido)

        ws['A1'] = 'Detalle Pedido '+str(ped.ped_id_Suc)+' N°'+ str(id_pedido)
        st=ws['A1']
        st.font = Font(size=14, b=True, color="004ee0")
        st.alignment = Alignment(horizontal='center')
        ws.merge_cells('A1:F1')
        ws.sheet_properties.tabColor = "1072BA"

        ws['A2'] = 'Producto'
        ws['B2'] = 'Descripcion'
        ws['C2'] = 'Sucursal'
        ws['D2'] = 'Cantidad'
        ws['E2'] = 'Precio'
        ws['F2'] = 'Total'
        cont = 3
        detalle=DetallePedido.objects.filter(dtl_id_pedido=id_pedido)
        for cto in detalle:
            ws.cell(row=cont, column=1).value = str(cto.dtl_codigo)
            ws.cell(row=cont, column=2).value = str(cto.dtl_descripcion)
            ws.cell(row=cont, column=3).value = str(cto.dtl_id_pedido.ped_id_Suc)
            ws.cell(row=cont, column=4).value = cto.dtl_cantidad
            ws.cell(row=cont, column=5).value = cto.dtl_precio
            ws.cell(row=cont, column=6).value = (cto.dtl_cantidad * cto.dtl_precio)
            ws.cell(row=cont, column=6).number_format = '#,##0'

            cont += 1

        ws["F"+str(cont)] = "=SUM(F3:F"+str(cont-1)+")"
        ws["F"+str(cont)].number_format = '#,##0'

        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    if cell.row != 1:
                        dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))

        for col, value in dims.items():
            ws.column_dimensions[get_column_letter(col)].width = value


        nombre_archivo='detalle_pedido_'+str(id_pedido)+'.xls'
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition']=content
        wb.save(response)
        return response

class DetallePedidolit(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pedido/ver_detalle.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        id_pedido=self.kwargs.get('pk')
        context['articulos']=DetallePedido.objects.filter(dtl_id_pedido=id_pedido)
        return context

class AutorizarPedido(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pedido/ver_detalle.html'
    def get(self, request , *args, **kwargs):
        import datetime
        ahora = datetime.datetime.now()
        id_pedido=self.kwargs.get('pk')
        Pedido.objects.filter(ped_id_ped=id_pedido).update(ped_estatusPedido=2, ped_id_UsuarioAutorizo=self.request.user, ped_fechaAutorizacion=ahora)
        rev=reverse_lazy('pedido:listar_pedido')
        return redirect(rev)

    @method_decorator(permission_required('pedido.change_pedido',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

class RechazarPedido(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pedido/ver_detalle.html'
    def get(self, request , *args, **kwargs):
        import datetime
        ahora = datetime.datetime.now()
        id_pedido=self.kwargs.get('pk')
        Pedido.objects.filter(ped_id_ped=id_pedido).update(ped_estatusPedido=4, ped_id_UsuarioCancelo=self.request.user, ped_fechaCancelacion=ahora)
        rev=reverse_lazy('pedido:listar_pedido')
        return redirect(rev)
    @method_decorator(permission_required('pedido.change_pedido',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

class PedidoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Pedido
    form_class = ProductoForm
    template_name ='pedido/pedido_form.html'
    success_url = reverse_lazy('pedido:listar_pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    def form_valid(self, form):
        import datetime
        ahora = datetime.datetime.now()
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.ped_estatusPedido = 3
        self.object.ped_fechaSubidaFac = ahora
        return super().form_valid(form)

    @method_decorator(permission_required('pedido.change_pedido',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

class PedidoDetalleList(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Pedido
    template_name = 'pedido/detalle_ped.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context
