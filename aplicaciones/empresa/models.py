from django.db import models
# Create your models here.
class Zona(models.Model):
    zona_nombre=models.CharField('Nombre', max_length=150)
    def __str__(self):
            return self.zona_nombre
    class Meta:
            ordering = ('zona_nombre',)

class Sucursal(models.Model):
    suc_id=models.AutoField(primary_key=True)
    suc_nombre=models.CharField('Nombre', max_length=150)
    suc_zona=models.ForeignKey(Zona, verbose_name='Pertenece zona', on_delete=models.CASCADE)
    suc_monto_papeleria=models.FloatField('Monto a comprar papeleria')
    suc_monto_limpieza=models.FloatField('Monto a comprar limpieza')
    suc_monto_limpieza_oficina=models.FloatField('Monto a comprar limpieza oficina', default=0)

    def __str__(self):
            return self.suc_nombre
    class Meta:
            ordering = ('suc_nombre',)


