# Generated by Django 2.1.7 on 2019-04-08 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0007_auto_20190401_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='ped_autorizo_fuera_tiempo',
            field=models.BooleanField(default=False),
        ),
    ]
