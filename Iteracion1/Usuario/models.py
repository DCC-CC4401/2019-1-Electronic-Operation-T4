from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    correo_Electrónico  = models.CharField(blank=False, null=False, max_length=50)
    nombre              = models.CharField(blank=False, null=False, max_length=30)
    apellido            = models.CharField(blank=False, null=False, max_length=30)
    contraseña          = models.CharField(blank=False, null=False, max_length=64)
    es_Admin            = models.BooleanField(blank=False, null=False, default=False)
    class Meta:
        unique_together = [['correo_Electrónico', 'nombre', 'apellido']]
