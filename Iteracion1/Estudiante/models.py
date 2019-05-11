from django.db import models
import uuid

# Create your models here.

""" Modelo de la entidad Estudiante para la base de datos
Fields:
    id          : (UUID) Identificador del registro
    id_Equipo   : (UUID) Referencia al equipo al que pertenece el estudiante
    historial   : (File) Archivo que contiene los equipos de los que ha formado parte el estudiante 
    Presentó    : (Boolean) Verdadero si el estudiante ha presentado, falso si no
    Nombre      : (String) Nombre del estudiante
    Notas       : (File) Archivo con las notas del alumno
Author:
    Claudio Mallea
"""
class Estudiante(models.Model):

    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_Equipo = models.ForeignKey('Equipo.Equipo', on_delete=models.CASCADE, blank=False, null=False)
    historial = models.FileField(upload_to=None, max_length=100)
    Presentó  = models.BooleanField(default=False)
    Nombre    = models.CharField(max_length=50, default="")
    Notas     = models.FileField(upload_to=None, max_length=100)
    class Meta:
        unique_together = [['id', 'id_Equipo']]