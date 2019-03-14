from django.db import models
from django.contrib.auth import get_user_model
Usuario = get_user_model()
# Create your models here.
class Sucursal(models.Model):
    suc_