from django.db import models
import uuid

# Create your models here.

""" Modelo de la entidad Nombre_Curso para la base de datos
Fields:
    id          : (UUID) Identificador del registro
    id_Curso    : (UUID) Identificador del curso al que nombra
    Nombre      : (Date) Nombre del curso
Author:
    Claudio Mallea
"""
class Nombre_Curso(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_Curso    = models.ForeignKey('Curso.Curso', on_delete=models.CASCADE, blank=False, null=False)
    Nombre      = models.CharField(max_length=100) 
    class Meta:
        unique_together = [['id', 'id_Curso']]