from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.empresa.models import Zona, Sucursal
from aplicaciones.empresa.forms import ZonaForm, SucursalForm
from django.urls import reverse_lazy
from aplicaciones.empresa.eliminaciones import get_deleted_objects
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
<<<<<<< HEAD
from aplicaciones.pedido.models import Producto, DetallePedido, Configuracion_pedido, Pedido, ConfigRestriccion
=======
from aplicaciones.pedido.models import Producto, DetallePedido, Configuracion_pedido, Pedido
>>>>>>> d0c7bc2272364b1328c755b79ca0818f46ba194e
from aplicaciones.pedido.forms import DetallePedidoForm
from django.http import JsonResponse
from django.db.models import Sum, F, Q, FloatField
from django.core.exceptions import ObjectDoesNotExist
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
        maximo_consumible=self.request.user.suc_pertene.suc_monto_consumible
        maximo_papeleria_consultorio=self.request.user.suc_pertene.suc_monto_papeleria_consultorio
        maximo_toner_consultorio=self.request.user.suc_pertene.suc_monto_toner_consultorio
        maximo_globos=self.request.user.suc_pertene.suc_monto_globos
<<<<<<< HEAD
        maximo_limpieza_oficina=self.request.user.suc_pertene.suc_monto_limpieza_oficina_v

        producto=Producto.objects.get(prod_codigo=codigo)
        mensaje, tipo_mensaje=createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, maximo_papeleria_consultorio, maximo_toner_consultorio, maximo_globos, maximo_limpieza_oficina, self)
=======

        producto=Producto.objects.get(prod_codigo=codigo)
        mensaje, tipo_mensaje=createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, maximo_papeleria_consultorio, maximo_toner_consultorio, maximo_globos, self)
>>>>>>> d0c7bc2272364b1328c755b79ca0818f46ba194e
        # try:
        #     get_gel_baterial = DetallePedido.objects.get(dtl_creado_por=self.request.user, dtl_status=False, dtl_codigo='019-068-611')
        #     mensaje='Solo se puede agregar una pieza 019-068-611' 
        #     tipo_mensaje=False
        #     if codigo != '019-068-611':
        #         mensaje, tipo_mensaje=createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, self)
        # except ObjectDoesNotExist:
        #     if codigo == '019-068-611':
        #         if int(cantidad) > 1:
        #             mensaje='Solo se puede agregar una pieza 019-068-611' 
        #             tipo_mensaje=False
        #         else:
        #             mensaje, tipo_mensaje=createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, self)
        #     else:    
        #         mensaje, tipo_mensaje=createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, self)

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



<<<<<<< HEAD
def createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, maximo_papeleria_consultorio, maximo_toner_consultorio, maximo_globos, maximo_limpieza_oficina, self):
=======
def createDetalleVenta(codigo, cantidad, tipo_pedido, maximo_papeleria, maximo_limpieza,  maximo_limpieza_consultorio, maximo_consumible, producto, maximo_papeleria_consultorio, maximo_toner_consultorio, maximo_globos, self):
>>>>>>> d0c7bc2272364b1328c755b79ca0818f46ba194e
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
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para papeleria' 
            tipo_mensaje=False
            return mensaje, tipo_mensaje

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
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para Limpieza'
            tipo_mensaje=False
            return mensaje, tipo_mensaje

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
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para Limpieza'
            tipo_mensaje=False
            return mensaje, tipo_mensaje

    elif tipo_pedido == '4':
        cuenta_now_limpieza=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=4, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
        if cuenta_now_limpieza['suma_total'] == None:
            cuenta_now_limpieza['suma_total']=0

        cutn_tem_limpieza = cuenta_now_limpieza['suma_total']+(producto.prod_precio * int(cantidad))
        if cutn_tem_limpieza <= maximo_consumible:
            det_pedido=DetallePedido(
                dtl_cantidad=cantidad,
                dtl_codigo=codigo,
                dtl_descripcion=producto.prod_descripcion,
                dtl_precio=producto.prod_precio,
                dtl_tipo=producto.prod_tipo,
                dtl_creado_por=self.request.user,
                dtl_tipo_pedido=4,
            )
            det_pedido.save()
            mensaje='Consumible OK'
            tipo_mensaje=True
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para Consumibles' 
            tipo_mensaje=False
            return mensaje, tipo_mensaje
    elif tipo_pedido == '5':
        cuenta_now_papeleria=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=5, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
        if cuenta_now_papeleria['suma_total'] == None:
            cuenta_now_papeleria['suma_total']=0

        cutn_tem_limpieza = cuenta_now_papeleria['suma_total']+(producto.prod_precio * int(cantidad))
        if cutn_tem_limpieza <= maximo_papeleria_consultorio:
            det_pedido=DetallePedido(
                dtl_cantidad=cantidad,
                dtl_codigo=codigo,
                dtl_descripcion=producto.prod_descripcion,
                dtl_precio=producto.prod_precio,
                dtl_tipo=producto.prod_tipo,
                dtl_creado_por=self.request.user,
                dtl_tipo_pedido=5,
            )
            det_pedido.save()
            mensaje='Papeleria consultorio OK'
            tipo_mensaje=True
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para papeleria consultorio' 
            tipo_mensaje=False
            return mensaje, tipo_mensaje
    elif tipo_pedido == '6':
        cuenta_now_papeleria=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=6, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
        if cuenta_now_papeleria['suma_total'] == None:
            cuenta_now_papeleria['suma_total']=0

        cutn_tem_limpieza = cuenta_now_papeleria['suma_total']+(producto.prod_precio * int(cantidad))
        if cutn_tem_limpieza <= maximo_toner_consultorio:
            det_pedido=DetallePedido(
                dtl_cantidad=cantidad,
                dtl_codigo=codigo,
                dtl_descripcion=producto.prod_descripcion,
                dtl_precio=producto.prod_precio,
                dtl_tipo=producto.prod_tipo,
                dtl_creado_por=self.request.user,
                dtl_tipo_pedido=6,
            )
            det_pedido.save()
            mensaje='Toner consultorio OK'
            tipo_mensaje=True
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para toner consultorio' 
            tipo_mensaje=False
            return mensaje, tipo_mensaje
    elif tipo_pedido == '7':
        cuenta_now=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=7, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
        if cuenta_now['suma_total'] == None:
            cuenta_now['suma_total']=0

        cutn_tem = cuenta_now['suma_total']+(producto.prod_precio * int(cantidad))
        if cutn_tem <= maximo_globos:
            det_pedido=DetallePedido(
                dtl_cantidad=cantidad,
                dtl_codigo=codigo,
                dtl_descripcion=producto.prod_descripcion,
                dtl_precio=producto.prod_precio,
                dtl_tipo=producto.prod_tipo,
                dtl_creado_por=self.request.user,
                dtl_tipo_pedido=7,
            )
            det_pedido.save()
            mensaje='Pedido globos OK'
            tipo_mensaje=True
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para pedidos globos' 
            tipo_mensaje=False
            return mensaje, tipo_mensaje

    elif tipo_pedido == '8':
        cuenta_now=DetallePedido.objects.filter(dtl_creado_por=self.request.user, dtl_tipo_pedido=8, dtl_status=False).aggregate(suma_total=Sum( F('dtl_cantidad')* F('dtl_precio'), output_field=FloatField() ))
        if cuenta_now['suma_total'] == None:
            cuenta_now['suma_total']=0

        cutn_tem = cuenta_now['suma_total']+(producto.prod_precio * int(cantidad))
        if cutn_tem <= maximo_limpieza_oficina:
            det_pedido=DetallePedido(
                dtl_cantidad=cantidad,
                dtl_codigo=codigo,
                dtl_descripcion=producto.prod_descripcion,
                dtl_precio=producto.prod_precio,
                dtl_tipo=producto.prod_tipo,
                dtl_creado_por=self.request.user,
                dtl_tipo_pedido=8,
            )
            det_pedido.save()
            mensaje='Pedido de limpieza oficina, OK'
            tipo_mensaje=True
            return mensaje, tipo_mensaje
        else:
            mensaje='Supera el máximo permitido para pedidos de limpieza oficina' 
            tipo_mensaje=False
            return mensaje, tipo_mensaje

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
<<<<<<< HEAD

=======
>>>>>>> d0c7bc2272364b1328c755b79ca0818f46ba194e
    def get_context_data(self, **kwargs):
        import datetime
        context = super().get_context_data(**kwargs)
        context['usuario']=self.request.user
        context['comparacion']=False
        context['conf_fecha']=Configuracion_pedido.objects.all()
        confs=Configuracion_pedido.objects.all()
        hoy=datetime.datetime.now()

<<<<<<< HEAD
        rangos_fehas = ConfigRestriccion.objects.filter(conf_r_fecha_inicio__lte=hoy, conf_r_fecha_fin__gte=hoy,
                                                        conf_r_tipo_pedido__exact=self.kwargs.get('tipo')).count()

        for config in confs:
            if config.conf_fecha_inicio <= hoy.date() <= config.conf_fecha_fin:
                context['comparacion'] = True

        if rangos_fehas > 0:
            context['comparacion'] = False

        return context

=======
        for config in confs:
            if config.conf_fecha_inicio <= hoy.date() and config.conf_fecha_fin >= hoy.date():
                context['comparacion']=True

        return context
>>>>>>> d0c7bc2272364b1328c755b79ca0818f46ba194e
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
            queryset = queryset.filter(prod_v_papeleria=True,prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=1, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            if pedido_count > 0:
                queryset = Producto.objects.none()
        elif tipo == 2:
            queryset = queryset.filter(prod_v_limpieza=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=2, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            if pedido_count > 0:
                queryset = Producto.objects.none()
        elif tipo == 3:
            queryset = queryset.filter(prod_v_limpieza_consultorio=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=3, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            
            if pedido_count > 0:
                queryset = Producto.objects.none()
        elif tipo == 4:
            queryset = queryset.filter(prod_v_consumibles=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=4, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            
            if pedido_count > 0:
                queryset = Producto.objects.none()
        elif tipo == 5:
            queryset = queryset.filter(prod_v_papeleria_consultorio=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=5, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            
            if pedido_count > 0:
                queryset = Producto.objects.none()
        elif tipo == 6:
            queryset = queryset.filter(prod_v_toner_consultorio=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=6, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            
            if pedido_count > 0:
                queryset = Producto.objects.none()
        elif tipo == 7:
            queryset = queryset.filter(prod_v_globos=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=7, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            
            if pedido_count > 0:
                queryset = Producto.objects.none()
<<<<<<< HEAD
        elif tipo == 8:
            queryset = queryset.filter(prod_v_limpieza_oficina=True, prod_estado_producto=True)
            pedido_count=Pedido.objects.filter(dtl_tipo_pedido=8, ped_id_Suc=self.request.user.suc_pertene, ped_fechaCreacion__range=(start_date,end_date)).count()
            
            if pedido_count > 0:
                queryset = Producto.objects.none()
=======
>>>>>>> d0c7bc2272364b1328c755b79ca0818f46ba194e

        return queryset


