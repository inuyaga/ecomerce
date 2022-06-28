from django.db import models
from django.contrib.auth.models import AbstractUser
from aplicaciones.empresa.models import Sucursal, Zona
class User(AbstractUser):
    TIPO_USER=((1,'Supervisor'), (2, 'Asesor'), (3, 'Usuario'))
    tipo_user = models.IntegerField(choices=TIPO_USER, default=3)
    zona_pertene = models.ForeignKey(Zona, verbose_name='Zona pertenece supervisor', on_delete=models.SET_NULL, blank=True, null=True)
    suc_pertene = models.ForeignKey(Sucursal, verbose_name='Sucursal pertenece usuario', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        ordering = ('-id',)

# Create your models here.
