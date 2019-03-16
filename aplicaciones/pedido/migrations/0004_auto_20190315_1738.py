# Generated by Django 2.1.5 on 2019-03-15 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_auto_20190315_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='ped_fechaSubidaFac',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Carga de factura'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='ped_pdffac',
            field=models.FileField(blank=True, null=True, upload_to='PdfFAC/', verbose_name='PDF de factura'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='ped_xmlfac',
            field=models.FileField(blank=True, null=True, upload_to='xmlFAC/', verbose_name='XML de factura'),
        ),
    ]