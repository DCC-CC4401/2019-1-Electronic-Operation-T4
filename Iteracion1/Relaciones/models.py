from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

""" Modelo de la relación Usuario_Evaluacion para la base de datos
Fields:
    id_Usuario      : (UUID) Identificador del evaluador
    id_Evaluacion   : (UUID) Identificador de la evaluación
Author:
    Clemente Paredes
"""
class Usuario_Evaluacion(models.Model):
    id_Usuario      = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    id_Evaluación   = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)

""" Modelo de la relación Usuario_Curso para la base de datos
Fields:
    id_Usuario : (UUID) Identificador del evaluador
    id_Curso   : (UUID) Identificador del curso
Author:
    Clemente Paredes
"""
class Usuario_Curso(models.Model):
    id_Usuario  = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    id_Curso    = models.ForeignKey('Curso.Curso', on_delete=models.CASCADE, blank=False, null=False)

""" Modelo de la relación Evaluacion_Equipo para la base de datos
Fields:
    id_Evaluacion   : (UUID) Identificador de la evaluación
    id_Equipo       : (UUID) Identificador del equipo evaluado
Author:
    Clemente Paredes
"""
class Evaluacion_Equipo(models.Model):
    id_Evaluación   = models.ForeignKey('Evaluacion.Evaluacion', on_delete=models.CASCADE, blank=False, null=False)
    id_Equipo       = models.ForeignKey('Equipo.Equipo', on_delete=models.CASCADE, blank=False, null=False)

""" Modelo de la relación Rubrica_Resumen para la base de datos
Fields:
    id_Rúbrica : (UUID) Identificador de la rúbrica
    id_Resumen : (UUID) Identificador del resumen
Author:
    Clemente Paredes
"""
class Rubrica_Resumen(models.Model):
    id_Rúbrica = models.ForeignKey('Rubrica.Rubrica', on_delete=models.CASCADE, blank=False, null=False)
    id_Resumen = models.ForeignKey('Resumen_Evaluacion.Resumen_Evaluacion', on_delete=models.CASCADE, blank=False, null=False)

""" Modelo de la relación Rubrica_Curso para la base de datos
Fields:
    id_Evaluacion   : (UUID) Identificador de la evaluación
    id_Curso        : (UUID) IDentificador del curso al que pertenece
Author:
    Nicolás Machuca
"""
class Evaluacion_Curso(models.Model):
    id_Evaluación = models.ForeignKey('Evaluacion.Evaluacion',  on_delete=models.CASCADE, blank=False, null=False)
    id_Curso = models.ForeignKey('Curso.Curso', on_delete=models.CASCADE, blank=False, null=False)

""" Modelo de la relación Evaluacion_Rubrica para la base de datos
Fields:
    id_Evaluacion   : (UUID) Identificador de la evaluación en curso
    id_Rúbrica      : (UUID) Identificador de la rúbrica
Author:
    Clemente Paredes y Nicolás Machuca
"""
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
