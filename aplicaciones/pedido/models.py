from django.db import models
from aplicaciones.empresa.models import Sucursal
from aplicaciones.usuario.models import User

class Producto(models.Model):
    prod_codigo = models.CharField('código del producto', max_length=11)
    prod_rutaimg=models.ImageField("imagen", upload_to="imgPrductos/", height_field=None, width_field=None, max_length=None)
    prod_descripcion=models.CharField('Descripción del producto', max_length=400)
    prod_precio=models.FloatField("Precio de producto")
    TIPOPRODUCTO=((1,"Papeleria"),(2,"Limpieza"))
    prod_tipo=models.IntegerField(choices=TIPOPRODUCTO)
    prod_estado_producto=models.BooleanField("Estatus del producto",default=True)
    def __str__(self):
            return self.prod_codigo

class Pedido(models.Model):
    ped_id_ped=models.AutoField(primary_key=True)
    ped_id_Suc=models.ForeignKey(Sucursal, verbose_name="Sucursales", on_delete=models.CASCADE)
    ped_fechaCreacion=models.DateTimeField("Fecha de creación", auto_now_add=True)
    ped_fechaAutorizacion= models.DateTimeField("Fecha de autorización")
    ped_fechaCancelacion= models.DateTimeField("Fecha de cancelación")
    ESTADOPEDIDO=((1,"Pendiente por autorizar"),(2,"Autorizado"),(3,"Facturado"),(4,"Rechazado"),(5,"Entregado"))
    ped_estatusPedido=models.IntegerField(choices=ESTADOPEDIDO)
    ped_id_UsuarioCreo=models.ForeignKey(User, verbose_name="Creador de pedido", related_name='creador', on_delete=models.SET_NULL,blank=True, null=True)
    ped_id_UsuarioAutorizo=models.ForeignKey(User, verbose_name="Autorizador",related_name='autorizador', on_delete=models.SET_NULL,blank=True, null=True)
    ped_id_UsuarioCancelo=models.ForeignKey(User, verbose_name="Cancelador",related_name='cancelo', on_delete=models.SET_NULL,blank=True, null=True)
    ped_pdffac=models.FileField("PDF de factura", upload_to="PdfFAC/", max_length=100)
    ped_xmlfac=models.FileField("XML de factura", upload_to="xmlFAC/", max_length=100)
    ped_fechaSubidaFac=models.DateTimeField("Carga de factura", auto_now=False, auto_now_add=False)
    def __str__(self):
        return str(self.ped_id_ped)

class DetallePedido(models.Model):
    dtl_id_detalle=models.AutoField(primary_key=True)
    dtl_id_pedido=models.ForeignKey(Pedido, verbose_name="Folio Pedido", on_delete=models.CASCADE)
    dtl_cantidad=models.IntegerField("Cantidad de producto")
    dtl_codigo = models.CharField('código del producto', max_length=11)
    dtl_descripcion=models.CharField('Descripción del producto', max_length=400)
    dtl_precio=models.FloatField("Precio de producto")
    TIPOPRODUCTO=((1,"Papeleria"),(2,"Limpieza"))
    dtl_tipo=models.IntegerField(choices=TIPOPRODUCTO)
    def __str__(self):
        return str(self.dtl_id_detalle)
    