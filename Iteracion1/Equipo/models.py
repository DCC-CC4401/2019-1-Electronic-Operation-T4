import uuid
from django.db import models

# Create your models here.

""" Modelo de la entidad Equipo para la base de datos
Fields:
    id          : (UUID) Identificador del registro
    id_Curso    : (UUID) Referencia al curso al que pertenece el equipo
    número      : (Int) Número del grupo
    nombre      : (String) Nombre del grupo
Author:
    Clemente Paredes
"""
class Equipo(models.Model):
    id       = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    id_Curso = models.ForeignKey('Curso.Curso', on_delete=models.CASCADE, blank=False, null=False)
    número   = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    nombre   = models.CharField(blank=False, null=False, default='Grupo 1', max_length=100)
    class Meta:
        unique_together = [['id_Curso', 'número']]