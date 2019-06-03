import uuid
from django.utils import timezone as tz
from django.db import models

# Create your models here.

""" Modelo de la entidad Curso para la base de datos
Fields:
    id              : (UUID) Identificador del registro
    código          : (String) Código del curso
    número_sección  : (Int) Número de la sección
    año             : (Int) Año de realización
    semestre        : (Int) Semestre de realización
Author:
    Clemente Paredes
"""
class Curso(models.Model):
    SEMESTRE_CHOICES = (
        (1, 'Otoño'),
        (2, 'Primavera'),
        (3, 'Verano')
    )
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    nombre          = models.CharField(max_length=100)
    código          = models.CharField(blank=False, null=False, max_length=20)
    número_sección  = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    año             = models.IntegerField(blank=False, null=False, default=tz.now().year)
    semestre        = models.SmallIntegerField(choices=SEMESTRE_CHOICES, default=1)
    class Meta:
        unique_together = [['código', 'número_sección', 'año', 'semestre']]
    def __str__(self):
        return self.nombre