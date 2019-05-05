import uuid
from django.utils import timezone as tz
from django import forms
from django.db import models

# Create your models here.
class Resumen_Evaluacion(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url                 = models.URLField(unique=True)
    id_Evaluacion       = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)
    fecha               = models.DateField(auto_now=False, auto_now_add=False, default=tz.now())
    contraseña          = models.CharField(max_length=50)
    duracion_Efectiva   = models.TimeField()
    class Meta:
        unique_together = [['url', 'id_Evaluacion']]