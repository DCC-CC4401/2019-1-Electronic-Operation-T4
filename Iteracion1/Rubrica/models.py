import uuid
from django.utils import timezone as tz
from django.db import models

# Create your models here.

""" Modelo de la entidad Rubrica para la base de datos
Fields:
    id              : (UUID) Identificador del registro
    nombre          : (String) Nombre de la rúbrica
    rúbrica         : (File) Archivo con la rúbrica
    duración_Mínima : (Time) Duración mínima de la evaluación
    duración_Máxima : (Time) Duración máxima de la evaluación
Author:
    Clemente Paredes
"""
class Rubrica(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre          = models.CharField(blank=False, default='Nombre de rúbrica', max_length=100)
    rúbrica         = models.FileField(upload_to=None, max_length=100)
    duración_Mínima = models.TimeField(blank=False, null=False, default=tz.now())
    duración_Máxima = models.TimeField(blank=False, null=False, default=tz.now())
    class Meta:
        unique_together = [['id', 'nombre']]