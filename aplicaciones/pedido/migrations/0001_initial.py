# Generated by Django 2.1.5 on 2019-03-14 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('dtl_id_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('dtl_cantidad', models.IntegerField(verbose_name='Cantidad de producto')),
                ('dtl_codigo', models.CharField(max_length=11, verbose_name='código del producto')),
                ('dtl_descripcion', models.CharField(max_length=400, verbose_name='Descripción del producto')),
                ('dtl_precio', models.FloatField(verbose_name='Precio de producto')),
                ('dtl_tipo', models.IntegerField(choices=[(1, 'Papeleria'), (2, 'Limpieza')])),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('ped_id_ped', models.AutoField(primary_key=True, serialize=False)),
                ('ped_fechaCreacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('ped_fechaAutorizacion', models.DateTimeField(verbose_name='Fecha de autorización')),
                ('ped_fechaCancelacion', models.DateTimeField(verbose_name='Fecha de cancelación')),
                ('ped_estatusPedido', models.IntegerField(choices=[(1, 'Pendiente por autorizar'), (2, 'Autorizado'), (3, 'Facturado'), (4, 'Rechazado'), (5, 'Entregado')])),
                ('ped_pdffac', models.FileField(upload_to='PdfFAC/', verbose_name='PDF de factura')),
                ('ped_xmlfac', models.FileField(upload_to='xmlFAC/', verbose_name='XML de factura')),
                ('ped_fechaSubidaFac', models.DateTimeField(verbose_name='Carga de factura')),
                ('ped_id_Suc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empresa.Sucursal', verbose_name='Sucursales')),
                ('ped_id_UsuarioAutorizo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='autorizador', to=settings.AUTH_USER_MODEL, verbose_name='Autorizador')),
                ('ped_id_UsuarioCancelo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cancelo', to=settings.AUTH_USER_MODEL, verbose_name='Cancelador')),
                ('ped_id_UsuarioCreo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creador', to=settings.AUTH_USER_MODEL, verbose_name='Creador de pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_codigo', models.CharField(max_length=11, verbose_name='código del producto')),
                ('prod_rutaimg', models.ImageField(upload_to='imgPrductos/', verbose_name='imagen')),
                ('prod_descripcion', models.CharField(max_length=400, verbose_name='Descripción del producto')),
                ('prod_precio', models.FloatField(verbose_name='Precio de producto')),
                ('prod_tipo', models.IntegerField(choices=[(1, 'Papeleria'), (2, 'Limpieza')])),
                ('prod_estado_producto', models.BooleanField(default=True, verbose_name='Estatus del producto')),
            ],
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='dtl_id_pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pedido.Pedido', verbose_name='Folio Pedido'),
        ),
    ]
