# Generated by Django 2.1.7 on 2019-04-01 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pedido', '0006_configuracion_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='ped_id_usr_descargo_excel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='descargo', to=settings.AUTH_USER_MODEL, verbose_name='Descargo'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='ped_estatusPedido',
            field=models.IntegerField(choices=[(1, 'Pendiente por autorizar'), (2, 'Autorizado'), (3, 'Facturado'), (4, 'Rechazado'), (5, 'Entregado'), (6, 'Excel descargado')], default=1),
        ),
    ]
