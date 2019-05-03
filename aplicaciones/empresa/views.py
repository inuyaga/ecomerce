from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.empresa.models import Zona, Sucursal
from aplicaciones.empresa.forms import ZonaForm, SucursalForm
from django.urls import reverse_lazy
from aplicaciones.empresa.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from aplicaciones.pedido.models import Producto, DetallePedido, Configuracion_pedido, Pedido
from aplicaciones.pedido.forms import DetallePedidoForm
from django.http import JsonResponse
from django.db.models import Sum, F, Q, FloatField
# Create your views here.


class inicio(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Producto
    paginate_by = 20
    template_name = 'admin/base_ecomer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        parametros = self.request.GET.copy()
        if parametros.get('filtro') != None:
            context['filtro'] = parametros.get('filtro')

        return context

    def get_queryset(self):
        queryset = super(inicio, self).get_queryset()
        if self.request.method == 'GET':
            filtro = self.request.GET.get('filtro')
            if filtro != None:
                queryset = queryset.filter(prod_tipo=filtro)

        return queryset




class DetallePedidoCreate(TemplateView):
    template_name = 'pedido/crear_producto.html'


    def post(self, request, *args, **kwargs):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        codigo = request.POST.get('dtl_codigo')
        cantidad = request.POST.get('dtl_cantidad')
        tipo_pedido = request.POST.get('dtl_tipo_pedido')

        mensaje=''
        pedido_conteo=0
        tipo_mensaje=False

        maximo_papeleria=self.request.user.suc_pertene.suc_monto_papeleria
        maximo_limpieza=self.request.user.suc_pertene.suc_monto_limpieza
        maximo_limpieza_consultorio=self.request.user.suc_pertene.suc_monto_limpieza_oficina

        producto=Producto.objects.get(prod_codigo=codigo)

        if tipo_pedido == '1':
            cuenta_now_papeleria=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=1,dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))

            if cuenta_now_papeleria['suma_total'] == None:
                cuenta_now_papeleria['suma_total']=0
            cutn_tem_papeleria = cuenta_now_papeleria['suma_total']+(producto.prod_precio * int(cantidad))

            if cutn_tem_papeleria <= maximo_papeleria:
                det_pedido=DetallePedido(
                dtl_cantidad=cantidad,
                dtl_codigo=codigo,
                dtl_descripcion=producto.prod_descripcion,
                dtl_precio=producto.prod_precio,
                dtl_tipo=producto.prod_tipo,
                dtl_creado_por=self.request.user,
                dtl_tipo_pedido=1,
                )
                det_pedido.save()
                mensaje='Papeleria Completado'
                tipo_mensaje=True
            else:
                mensaje='Supera el máximo permitido para papeleria'
                tipo_mensaje=False

        elif tipo_pedido == '2':
            cuenta_now_limpieza=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=2, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
            if cuenta_now_limpieza['suma_total'] == None:
                cuenta_now_limpieza['suma_total']=0

            cutn_tem_limpieza = cuenta_now_limpieza['suma_total']+(producto.prod_precio * int(cantidad))
            if cutn_tem_limpieza <= maximo_limpieza:
                det_pedido=DetallePedido(
                    dtl_cantidad=cantidad,
                    dtl_codigo=codigo,
                    dtl_descripcion=producto.prod_descripcion,
                    dtl_precio=producto.prod_precio,
                    dtl_tipo=producto.prod_tipo,
                    dtl_creado_por=self.request.user,
                    dtl_tipo_pedido=2,
                )
                det_pedido.save()
                mensaje='Limpieza OK'
                tipo_mensaje=True
            else:
                mensaje='Supera el máximo permitido para Limpieza'
                tipo_mensaje=False

        elif tipo_pedido == '3':
            cuenta_now_limpieza=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=3, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
            if cuenta_now_limpieza['suma_total'] == None:
                cuenta_now_limpieza['suma_total']=0

            cutn_tem_limpieza = cuenta_now_limpieza['suma_total']+(producto.prod_precio * int(cantidad))
            if cutn_tem_limpieza <= maximo_limpieza_consultorio:
                det_pedido=DetallePedido(
                    dtl_cantidad=cantidad,
                    dtl_codigo=codigo,
                    dtl_descripcion=producto.prod_descripcion,
                    dtl_precio=producto.prod_precio,
                    dtl_tipo=producto.prod_tipo,
                    dtl_creado_por=self.request.user,
                    dtl_tipo_pedido=3,
                )
                det_pedido.save()
                mensaje='Limpieza OK'
                tipo_mensaje=True
            else:
                mensaje='Supera el máximo permitido para Limpieza'
                tipo_mensaje=False




        json = JsonResponse(
            {
                'content':{
                    'mensaje': mensaje,
                    'conteo': pedido_conteo,
                    'tipo_mensaje': tipo_mensaje,
                }
            }
        )
        return json



class ZonaCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Zona
    template_name = 'ecomer/crear_zona.html'
    form_class = ZonaForm
    success_url = reverse_lazy('empresa:list_zona')

    @method_decorator(permission_required('empresa.add_zona',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaCreate, self).dispatch(*args, **kwargs)

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

    def get_queryset(self):
        queryset = super(ZonaList, self).get_queryset()
        busqueda=self.request.GET.get('buscar')
        if busqueda != None:
            queryset=queryset.filter(zona_nombre__icontains=busqueda)
        return queryset

    @method_decorator(permission_required('empresa.view_zona',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaList, self).dispatch(*args, **kwargs)

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

    @method_decorator(permission_required('empresa.change_zona',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaUpdate, self).dispatch(*args, **kwargs)


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

    @method_decorator(permission_required('empresa.delete_zona',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(ZonaDelete, self).dispatch(*args, **kwargs)

class SucursalList(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Sucursal
    template_name = 'ecomer/sucursales_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        return context

    def get_queryset(self):
        queryset = super(SucursalList, self).get_queryset()
        busqueda=self.request.GET.get('buscar')
        if busqueda != None:
            queryset=queryset.filter(Q(suc_nombre__icontains=busqueda) | Q(suc_zona__zona_nombre__icontains=busqueda))
        return queryset

    @method_decorator(permission_required('empresa.view_sucursal',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(SucursalList, self).dispatch(*args, **kwargs)

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
    @method_decorator(permission_required('empresa.add_sucursal',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(SucursalCreate, self).dispatch(*args, **kwargs)

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

    @method_decorator(permission_required('empresa.change_sucursal',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(SucursalUpdate, self).dispatch(*args, **kwargs)


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

    @method_decorator(permission_required('empresa.delete_sucursal',reverse_lazy('requiere_permisos')))
    def dispatch(self, *args, **kwargs):
                return super(SucursalDelete, self).dispatch(*args, **kwargs)




class PedidoCompraSuc(ListView):
    model=Producto
    paginate_by=20
    template_name='pedido/pedido_limpieza.html'
    def get_context_data(self, **kwargs):
        import datetime
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        context['comparacion']=False
        context['conf_fecha']=Configuracion_pedido.objects.all()
        confs=Configuracion_pedido.objects.all()
        hoy=datetime.datetime.now()

        for config in confs:
            if config.conf_fecha_inicio <= hoy.date() and config.conf_fecha_fin >= hoy.date():
                context['comparacion']=True

        return context
    def get_queryset(self):
        from datetime import datetime, date
        import calendar
        # ESTABLECEMOS LA FECHA ACTUAL
        today = datetime.now()
        # CONSULTAMOS CUAL ES EL ULTIMO DIA DEL MES ACTUAL
        last_day=calendar.monthrange(today.year, today.month)[1]
        # INICIALIZAMOS LA FECHA INICIAL
        start_date = datetime(today.year, today.month, 1)
        # INICIALIZAMOS LA FECHA FINAL
        end_date = datetime(today.year, today.month, last_day)
        

        queryset = super(PedidoCompraSuc, self).get_queryset()
        tipo = self.kwargs['tipo']
        if tipo == 1:
            queryset = queryset.filter(prod_tipo=1,prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=1, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            if pedido_count > 0:
                queryset = ''
        elif tipo == 2:
            queryset = queryset.filter(prod_tipo=2, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=2, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            if pedido_count > 0:
                queryset = ''
        elif tipo == 3:
            queryset = queryset.filter(prod_tipo=2, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=3, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            if pedido_count > 0:
                queryset = ''
            
            
            
            

        return queryset


