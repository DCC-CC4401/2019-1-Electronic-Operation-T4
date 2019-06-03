from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class Usuario_Evaluacion(models.Model):
    id_Usuario      = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    id_Evaluación   = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)

class Evaluacion_Equipo(models.Model):
    id_Evaluación   = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)
    id_Equipo       = models.ForeignKey('Equipo.Equipo', on_delete=models.CASCADE, blank=False, null=False)

class Rubrica_Resumen(models.Model):
    id_Rúbrica = models.ForeignKey('Rubrica.Rubrica', on_delete=models.CASCADE, blank=False, null=False)
    id_Resumen = models.ForeignKey('Resumen_Evaluacion.Resumen_Evaluacion', on_delete=models.CASCADE, blank=False, null=False)

class Evaluacion_Curso(models.Model):
    id_Evaluación = models.ForeignKey('Evaluacion.Evaluacion',  on_delete=models.CASCADE, blank=False, null=False)
    id_Curso = models.ForeignKey('Curso.Curso', on_delete=models.CASCADE, blank=False, null=False)

class Evaluacion_Rubrica(models.Model):
    id_Evaluación = models.ForeignKey('Evaluacion.Evaluacion',  on_delete=models.CASCADE, blank=False, null=False)
    id_Rúbrica = models.ForeignKey('Rubrica.Rubrica', on_delete=models.CASCADE, blank=False, null=False)


""" Modelo de la relación Evaluacion_Estudiante para la base de datos
Fields:
    id_Evaluacion   : (UUID) Identificador de la evaluación en curso
    id_Estudiante     : (UUID) Identificador del estudiante
Author:
    Nicolás Machuca
"""
class Evaluacion_Estudiante(models.Model):
    id_Evaluación = models.ForeignKey('Evaluacion.Evaluacion',  on_delete=models.CASCADE, blank=False, null=False)
    id_Estudiante = models.ForeignKey('Estudiante.Estudiante', on_delete=models.CASCADE, blank=False, null=False)
