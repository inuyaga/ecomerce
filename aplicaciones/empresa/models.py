from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()
# Create your models here.
class Zona(models.Model):
    zona_nombre=models.CharField('Nombre', max_length=150)
    zona_supervisor=models.OneToOneField(Usuario, verbose_name='Supervisor', on_delete=models.CASCADE)


class Sucursal(models.Model):
    suc_id=models.AutoField(primary_key=True)
    suc_nombre=models.CharField('Nombre', max_length=150)
    suc_zona=models.ForeignKey(Zona, verbose_name='Pertenece zona', on_delete=models.CASCADE)
    suc_monto_papeleria=models.FloatField('Monto a comprar papeleria')
    suc_monto_limpieza=models.FloatField('Monto a comprar limpieza')
    suc_usuario=models.OneToOneField(Usuario, verbose_name='Encargado', on_delete=models.CASCADE)
