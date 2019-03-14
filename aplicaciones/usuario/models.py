from django.db import models
from django.contrib.auth.models import AbstractUser
from aplicaciones.empresa.models import Sucursal, Zona
class User(AbstractUser):
    TIPO_USER=((1,'Supervisor'), (2, 'Usuario'))
    tipo_user = models.IntegerField(choices=TIPO_USER, default=1)
    zona_pertene = models.OneToOneField(Zona, verbose_name='Zona pertenece supervisor', on_delete=models.SET_NULL, blank=True, null=True)
    suc_pertene = models.OneToOneField(Sucursal, verbose_name='Sucursal pertenece usuario', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
# Create your models here.
