from django.db import models 
from django.db.models import Sum, F, FloatField
from aplicaciones.empresa.models import Sucursal
from aplicaciones.usuario.models import User
from django.utils import timezone
TIPO_PEDIDO=((1,"Papeleria"),(2,"Limpieza"), (3,"Limpieza Consultorio"), (4,"Toner"), (5,"Papeleria consultorio"))
class Producto(models.Model): 
    prod_codigo = models.CharField('código del producto', max_length=11, unique=True)
    prod_rutaimg=models.ImageField("imagen", upload_to="imgPrductos/")
    prod_descripcion=models.CharField('Descripción del producto', max_length=400)
    prod_precio=models.FloatField("Precio de producto")
    
    prod_tipo=models.IntegerField('Tipo de producto', choices=TIPO_PEDIDO)
    prod_estado_producto=models.BooleanField("Estatus del producto",default=True)

    prod_v_papeleria=models.BooleanField('Visible en papeleria',default=False)
    prod_v_limpieza=models.BooleanField('Visible en Limpieza',default=False)
    prod_v_limpieza_consultorio=models.BooleanField('Visible en Limpieza Consultorio',default=False)
    prod_v_papeleria_consultorio=models.BooleanField('Visible en papeleria Consultorio',default=False)
    prod_v_consumibles=models.BooleanField('Visible en Toner',default=False)
    def __str__(self):
            return self.prod_codigo

class Pedido(models.Model):  
    ped_id_ped=models.AutoField(primary_key=True)
    ped_id_Suc=models.ForeignKey(Sucursal, verbose_name="Sucursales", on_delete=models.CASCADE)
    ped_fechaCreacion=models.DateField("Fecha de creación", auto_now_add=True)
    ped_fechaAutorizacion= models.DateTimeField("Fecha de autorización",blank=True, null=True)
    ped_fechaCancelacion= models.DateTimeField("Fecha de cancelación",blank=True, null=True) 
    ESTADOPEDIDO=((1,"Pendiente por autorizar"),(2,"Autorizado"),(3,"Facturado"),(4,"Rechazado"),(5,"Entregado"), (6,"Excel descargado"))
    ped_estatusPedido=models.IntegerField(choices=ESTADOPEDIDO, default=1)
    ped_autorizo_fuera_tiempo=models.BooleanField(default=False)
    ped_id_UsuarioCreo=models.ForeignKey(User, verbose_name="Creador de pedido", related_name='creador', on_delete=models.SET_NULL,blank=True, null=True)
    ped_id_UsuarioAutorizo=models.ForeignKey(User, verbose_name="Autorizador",related_name='autorizador', on_delete=models.SET_NULL,blank=True, null=True)
    ped_id_UsuarioCancelo=models.ForeignKey(User, verbose_name="Cancelador",related_name='cancelo', on_delete=models.SET_NULL,blank=True, null=True)
    ped_id_usr_descargo_excel=models.ForeignKey(User, verbose_name="Descargo",related_name='descargo', on_delete=models.SET_NULL,blank=True, null=True)
    ped_pdffac=models.FileField("PDF de factura", upload_to="PdfFAC/", max_length=100,blank=True, null=True)
    ped_xmlfac=models.FileField("XML de factura", upload_to="xmlFAC/", max_length=100,blank=True, null=True)
    ped_fechaSubidaFac=models.DateTimeField("Carga de factura", blank=True, null=True)
    
    dtl_tipo_pedido=models.IntegerField(choices=TIPO_PEDIDO, default=0)
    TIPO_INSUMO=((800044556,"Insumos Pedido Mensual"),(800044563,"Papeleria Pedido Mensual"))
    pedido_tipo_insumo=models.IntegerField(choices=TIPO_INSUMO, default=800044556)
    def __str__(self):
        return str(self.ped_id_ped)
    
    def total_venta(self):
        query=DetallePedido.objects.filter(dtl_id_pedido=self.ped_id_ped).aggregate(total_venta=Sum(F('dtl_cantidad') * F('dtl_precio'), output_field=FloatField()))
        return 0 if query['total_venta'] == None else round(query['total_venta'], 3)

class DetallePedido(models.Model):
    dtl_id_detalle=models.AutoField(primary_key=True)
    dtl_id_pedido=models.ForeignKey(Pedido, verbose_name="Folio Pedido", blank=True, null=True, on_delete=models.CASCADE)
    dtl_cantidad=models.IntegerField("Cantidad de producto")
    dtl_codigo = models.CharField('código del producto', max_length=11)
    dtl_descripcion=models.CharField('Descripción del producto', max_length=400)
    dtl_precio=models.FloatField("Precio de producto")
    TIPOPRODUCTO=((1,"Papeleria"),(2,"Limpieza"))
    dtl_tipo=models.IntegerField(choices=TIPOPRODUCTO)    
    dtl_tipo_pedido=models.IntegerField(choices=TIPO_PEDIDO, default=0)
    dtl_creado_por = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    dtl_status=models.BooleanField('status', default=False)

    def __str__(self):
        return str(self.dtl_id_detalle)

    def total(self):
        suma=self.dtl_cantidad * self.dtl_precio
        return suma

class Configuracion_pedido(models.Model):
    conf_ID=models.AutoField(primary_key=True)
    conf_fecha_inicio=models.DateField('Fecha inicio')
    conf_fecha_fin=models.DateField('Fecha final')
    conf_fecha_fin_autorizador=models.DateField('Fecha final para autorizar', default=timezone.now)


