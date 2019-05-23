from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, DetailView, View
from aplicaciones.pedido.models import *
from aplicaciones.pedido.forms import *
from django.urls import reverse_lazy, reverse
from aplicaciones.empresa.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from openpyxl.styles import Font, Fill, Alignment
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q
from django.http import JsonResponse


class ProductoLista(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Producto
    paginate_by = 250
    template_name = 'pedido/productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_queryset(self):
        queryset = super(ProductoLista, self).get_queryset()
        buesqueda = self.request.GET.get('search')
        if buesqueda != None:
            queryset = queryset.filter(Q(prod_codigo=buesqueda) | Q(
                prod_descripcion__icontains=buesqueda))

        return queryset


class PrductoCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Producto
    form_class = ProductoForm
    template_name = 'pedido/crear_producto.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    @method_decorator(permission_required('pedido.add_producto', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(PrductoCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
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
        context['usuario'] = self.request.user
        return context

    @method_decorator(permission_required('pedido.change_producto', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(ProductoUpdate, self).dispatch(*args, **kwargs)


class ProductoDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Producto
    template_name = 'eliminaciones.html'
    success_url = reverse_lazy('pedido:ProductoLista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context

    @method_decorator(permission_required('pedido.delete_producto', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(ProductoDelete, self).dispatch(*args, **kwargs)


class PedidoList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Pedido
    template_name = 'pedido/pedido_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_queryset(self):
        queryset = super(PedidoList, self).get_queryset()
        status = self.request.GET.get('status')
        tipo_pedido = self.request.GET.get('tipo_pedido')

        if self.request.user.is_superuser or self.request.user.tipo_user == 2:
            queryset = queryset.filter(ped_estatusPedido=1)
            if status != None:
                queryset = Pedido.objects.filter(ped_estatusPedido=status)
                if status == '0':
                    queryset = Pedido.objects.all()
            if tipo_pedido != None:
                queryset = queryset.filter(dtl_tipo_pedido=tipo_pedido)

        elif self.request.user.tipo_user == 1:
            id_zona = self.request.user.zona_pertene
            queryset_init = queryset.filter(ped_id_Suc__suc_zona=id_zona)
            queryset = queryset.filter(
                ped_id_Suc__suc_zona=id_zona, ped_estatusPedido=1)

            if status != None:
                queryset = queryset_init.filter(ped_estatusPedido=status)
                if status == '0':
                    queryset = queryset_init
            if tipo_pedido != None:
                queryset = queryset.filter(dtl_tipo_pedido=tipo_pedido)

        elif self.request.user.tipo_user == 3:
            id_suc = self.request.user.suc_pertene
            queryset_init = queryset.filter(ped_id_Suc=id_suc)
            queryset = queryset.filter(ped_id_Suc=id_suc, ped_estatusPedido=1)

            if status != None:
                queryset = queryset_init.filter(ped_estatusPedido=status)
                if status == '0':
                    queryset = queryset_init
            if tipo_pedido != None:
                queryset = queryset.filter(dtl_tipo_pedido=tipo_pedido)

        return queryset


class CarritoLista(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = DetallePedido
    template_name = 'pedido/carrito.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['ped_papeleria'] = DetallePedido.objects.filter(
            dtl_creado_por=self.request.user, dtl_status=False, dtl_tipo_pedido=1)
        context['ped_lim_consultorio'] = DetallePedido.objects.filter(
            dtl_creado_por=self.request.user, dtl_status=False, dtl_tipo_pedido=3)
        context['ped_lim_sucursal'] = DetallePedido.objects.filter(
            dtl_creado_por=self.request.user, dtl_status=False, dtl_tipo_pedido=2)

        return context

    def get_queryset(self):
        queryset = super(CarritoLista, self).get_queryset()
        queryset = queryset.filter(
            dtl_creado_por=self.request.user, dtl_status=False)
        return queryset

    def post(self, request, *args, **kwargs):

        tipo_pedido = request.POST.get('tipo_pedido')

        if tipo_pedido == 'papeleria':
            pedido = Pedido(
                ped_id_Suc=self.request.user.suc_pertene,
                ped_id_UsuarioCreo=self.request.user,
                dtl_tipo_pedido=1,
                pedido_tipo_insumo=800044563,
            )
            pedido.save()

            DetallePedido.objects.filter(
                dtl_creado_por=self.request.user,
                dtl_status=False, dtl_tipo_pedido=1).update(dtl_status=True, dtl_id_pedido=pedido)
        if tipo_pedido == 'sucursal':
            pedido = Pedido(
                ped_id_Suc=self.request.user.suc_pertene,
                ped_id_UsuarioCreo=self.request.user,
                dtl_tipo_pedido=2,
            )
            pedido.save()
            DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_status=False, dtl_tipo_pedido=2).update(
                dtl_status=True, dtl_id_pedido=pedido)
        if tipo_pedido == 'consultorio':
            pedido = Pedido(
                ped_id_Suc=self.request.user.suc_pertene,
                ped_id_UsuarioCreo=self.request.user,
                dtl_tipo_pedido=3,
            )
            pedido.save()
            DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_status=False, dtl_tipo_pedido=3).update(
                dtl_status=True, dtl_id_pedido=pedido)

        url = reverse_lazy('pedido:carrito')
        return redirect(url)


class CarritoDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = DetallePedido
    template_name = 'eliminaciones.html'
    success_url = reverse_lazy('pedido:carrito')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        deletable_objects, model_count, protected = get_deleted_objects([
                                                                        self.object])
        context['deletable_objects'] = deletable_objects
        context['model_count'] = dict(model_count).items()
        context['protected'] = protected
        return context


class DowloadExcelPedido(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        from openpyxl.utils import get_column_letter
        import datetime
        wb = Workbook()
        ws = wb.active
        id_pedido = self.kwargs.get('pk')
        ped = Pedido.objects.get(ped_id_ped=id_pedido)

        ws['A1'] = 'Detalle Pedido '+str(ped.ped_id_Suc)+' N°' + str(id_pedido)
        st = ws['A1']
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
        detalle = DetallePedido.objects.filter(dtl_id_pedido=id_pedido)
        for cto in detalle:
            ws.cell(row=cont, column=1).value = str(cto.dtl_codigo)
            ws.cell(row=cont, column=2).value = str(cto.dtl_descripcion)
            ws.cell(row=cont, column=3).value = str(
                cto.dtl_id_pedido.ped_id_Suc)
            ws.cell(row=cont, column=4).value = cto.dtl_cantidad
            ws.cell(row=cont, column=5).value = cto.dtl_precio
            ws.cell(row=cont, column=6).value = (
                cto.dtl_cantidad * cto.dtl_precio)
            ws.cell(row=cont, column=6).number_format = '#,##0'

            cont += 1

        ws["F"+str(cont)] = "=SUM(F3:F"+str(cont-1)+")"
        ws["F"+str(cont)].number_format = '#,##0'

        dims = {}
        for row in ws.rows:
            for cell in row:
                if cell.value:
                    if cell.row != 1:
                        dims[cell.column] = max(
                            (dims.get(cell.column, 0), len(str(cell.value))))

        for col, value in dims.items():
            ws.column_dimensions[get_column_letter(col)].width = value

        ahora = datetime.datetime.now()
        Pedido.objects.filter(ped_id_ped=id_pedido).update(
            ped_estatusPedido=6, ped_id_usr_descargo_excel=self.request.user)
        nombre_archivo = 'pedido_no_'+str(id_pedido)+'.xls'
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response


class DetallePedidolit(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pedido/ver_detalle.html' 

    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        id_pedido = self.kwargs.get('pk')
        context['articulos'] = DetallePedido.objects.filter(
            dtl_id_pedido=id_pedido)
        context['suma_total'] = DetallePedido.objects.filter(
            dtl_id_pedido=id_pedido).aggregate(Sum('dtl_precio'))
        context['suma_total_partids'] = DetallePedido.objects.filter(
            dtl_id_pedido=id_pedido).aggregate(Sum('dtl_cantidad'))
        return context


class DetallePeditoEliminar(DeleteView):
    model = DetallePedido
    template_name = 'eliminaciones.html'
    success_url = reverse_lazy('pedido:detalle_pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self):
        slug = self.kwargs['pedo_id']
        link = reverse_lazy('pedido:detalle_pedido', kwargs={'pk': slug})
        return link

    @method_decorator(permission_required('pedido.delete_detallepedido', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(DetallePeditoEliminar, self).dispatch(*args, **kwargs)


class DetallePedidoEdit(UpdateView):
    model = DetallePedido
    template_name = 'pedido/conf_create.html'
    form_class = DetallePedidoFormEdit
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def get_success_url(self):
        slug = self.kwargs['pedo_id']
        link = reverse_lazy('pedido:detalle_pedido', kwargs={'pk': slug})
        return link

    @method_decorator(permission_required('pedido.change_detallepedido', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(DetallePedidoEdit, self).dispatch(*args, **kwargs)


class AutorizarPedido(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pedido/ver_detalle.html'

    def get(self, request, *args, **kwargs):
        from datetime import datetime
        ahora = datetime.now()
        id_pedido = self.kwargs.get('pk')
        confs = Configuracion_pedido.objects.all()
        for config in confs:
            if ahora.date() <= config.conf_fecha_fin_autorizador:
                Pedido.objects.filter(ped_id_ped=id_pedido).update(
                    ped_estatusPedido=2, ped_id_UsuarioAutorizo=self.request.user, ped_fechaAutorizacion=ahora)
            else:
                Pedido.objects.filter(ped_id_ped=id_pedido).update(
                    ped_estatusPedido=2, ped_id_UsuarioAutorizo=self.request.user, ped_fechaAutorizacion=ahora, ped_autorizo_fuera_tiempo=True)

        rev = reverse_lazy('pedido:listar_pedido')
        return redirect(rev)

    @method_decorator(permission_required('pedido.change_pedido', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(AutorizarPedido, self).dispatch(*args, **kwargs)


class RechazarPedido(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'pedido/ver_detalle.html'

    def get(self, request, *args, **kwargs):
        import datetime
        ahora = datetime.datetime.now()
        id_pedido = self.kwargs.get('pk')
        Pedido.objects.filter(ped_id_ped=id_pedido).update(
            ped_estatusPedido=4, ped_id_UsuarioCancelo=self.request.user, ped_fechaCancelacion=ahora)

        rev = reverse_lazy('pedido:listar_pedido')
        return redirect(rev)

    @method_decorator(permission_required('pedido.change_pedido', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(RechazarPedido, self).dispatch(*args, **kwargs)


class PedidoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido/pedido_form.html'
    success_url = reverse_lazy('pedido:listar_pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

    def form_valid(self, form):
        import datetime
        ahora = datetime.datetime.now()
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.object.ped_estatusPedido = 3
        self.object.ped_fechaSubidaFac = ahora
        return super().form_valid(form)

    @method_decorator(permission_required('pedido.change_pedido', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(PedidoUpdate, self).dispatch(*args, **kwargs)


class PedidoDetalleList(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Pedido
    template_name = 'pedido/detalle_ped.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class ConfiguracionList(ListView):
    model = Configuracion_pedido
    template_name = 'pedido/conf_pedido.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class ConfigCreate(CreateView):
    model = Configuracion_pedido
    form_class = ConfForm
    template_name = 'pedido/conf_create.html'
    success_url = reverse_lazy('pedido:configuracion_pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class ConfigUpdate(UpdateView):
    model = Configuracion_pedido
    form_class = ConfFormEdit
    template_name = 'pedido/conf_create.html'
    success_url = reverse_lazy('pedido:configuracion_pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context


class PedidoDeleteRechazado(TemplateView):
    template_name = 'eliminacion_masiva.html'

    def post(self, request, *args, **kwargs):
        Pedido.objects.filter(ped_estatusPedido=4).delete()
        url = reverse_lazy('pedido:listar_pedido')
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['dell_masivo_list'] = Pedido.objects.filter(
            ped_estatusPedido=4)

        return context

    @method_decorator(permission_required('pedido.delete_pedido', reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
        return super(PedidoDeleteRechazado, self).dispatch(*args, **kwargs)


class GeneraValuesJsonPedidos(View):
    def post(self, request, *args, **kwargs):
        import json
        from datetime import datetime
        body = json.loads(request.body)
        inicio = body.get('fecha_inicio')
        fin =body.get('fecha_fin')

        if inicio == '' or fin == '':
            data = {
                'msn': 'Debe de indicar las dos fechas',
                'status': False,
            }
            return JsonResponse(data, status=400)
        else:
            inicio = datetime.strptime(body.get('fecha_inicio'), '%Y-%m-%d')
            fin = datetime.strptime(body.get('fecha_fin'), '%Y-%m-%d')
            if fin > inicio:
                query=Pedido.objects.filter(ped_fechaCreacion__range=[inicio, fin]).values(
                    'ped_id_ped',
                    'ped_id_Suc__suc_numero',
                    'ped_id_Suc__suc_nombre',
                    'ped_id_Suc__suc_direccion',
                    'pedido_tipo_insumo',
                )
                lista=list(query)
                data = {
                    'obj_list': lista,
                    'status': True,
                }
                return JsonResponse(data)
            else:
                data = {
                    'msn': 'La fecha inicial no puede ser mayor o igual a la fecha final',
                    'status': False,
                }
                return JsonResponse(data, status=400)
