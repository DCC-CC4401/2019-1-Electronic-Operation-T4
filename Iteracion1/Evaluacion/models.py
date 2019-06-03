import uuid
from django.utils import timezone as tz
from django.db import models

# Create your models here.
class Evaluacion(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_Curso            = models.ForeignKey('Curso.Curso', on_delete=models.CASCADE, blank=False, null=True)
    nombre              = models.CharField(blank=False, default='Evaluacion default', max_length=100)
    fecha_Inicio        = models.DateField(auto_now=False, auto_now_add=False, default=tz.now())
    fecha_Fin           = models.DateField(auto_now=False, auto_now_add=False, default=tz.now())
    is_Open             = models.BooleanField(default=True)
    is_Editable         = models.BooleanField(default=True)
    equipo_Presentando  = models.ForeignKey('Equipo.Equipo', on_delete=models.SET_NULL, blank=False, null=True)