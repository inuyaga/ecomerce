from django.db import models
from aplicaciones.empresa.models import Sucursal
from aplicaciones.usuario.models import User

class Producto(models.Model):
    codigo = models.CharField('código del producto', max_length=11)
    rutaimg=models.ImageField("imagen", upload_to="imgPrductos/", height_field=None, width_field=None, max_length=None)
    descripcion=models.CharField('Descripción del producto', max_length=400)
    precio=models.FloatField("Precio de producto")
    TIPOPRODUCTO=((1,"Papeleria"),(2,"Limpieza"))
    tipo=models.IntegerField(choices=TIPOPRODUCTO)
    estado_producto=models.BooleanField("Estatus del producto",default=True)
    def __str__(self):
            return self.codigo

class Pedido(models.Model):
    id_ped=models.AutoField(primary_key=True)
    id_Suc=models.ForeignKey(Sucursal, verbose_name="Sucursales", on_delete=models.CASCADE)
    fechaCreacion=models.DateTimeField("Fecha de creación", auto_now_add=True)
    fechaAutorizacion= models.DateTimeField("Fecha de autorización")
    fechaCancelacion= models.DateTimeField("Fecha de cancelación")
    ESTADOPEDIDO=((1,"Pendiente por autorizar"),(2,"Autorizado"),(3,"Facturado"),(4,"Rechazado"),(5,"Entregado"))
    estatusPedido=models.IntegerField(choices=ESTADOPEDIDO)
    id_UsuarioCreo=models.ForeignKey(User, verbose_name="Creador de pedido", on_delete=models.SET_NULL,blank=True, null=True)
    id_UsuarioAutorizo=models.ForeignKey(User, verbose_name="Autorizador", on_delete=models.SET_NULL,blank=True, null=True)
    id_UsuarioCancelo=models.ForeignKey(User, verbose_name="Cancelador", on_delete=models.SET_NULL,blank=True, null=True)
    pdffac=models.FileField("PDF de factura", upload_to="PdfFAC/", max_length=100)
    xmlfac=models.FileField("XML de factura", upload_to="xmlFAC/", max_length=100)
    fechaSubidaFac=models.DateTimeField("Carga de factura", auto_now=False, auto_now_add=False)
    def __str__(self):
        return str(self.id_ped)

class DetallePedido(models.Model):
    id_detalle=models.AutoField(primary_key=True)
    id_pedido=models.ForeignKey(Pedido, verbose_name="Folio Pedido", on_delete=models.CASCADE)
    cantidad=models.IntegerField("Cantidad de producto")
    codigo = models.CharField('código del producto', max_length=11)
    descripcion=models.CharField('Descripción del producto', max_length=400)
    precio=models.FloatField("Precio de producto")
    TIPOPRODUCTO=((1,"Papeleria"),(2,"Limpieza"))
    tipo=models.IntegerField(choices=TIPOPRODUCTO)
    def __str__(self):
        return str(self.id_detalle)
    