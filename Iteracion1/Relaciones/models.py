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


"""
Modelo de la relacion Evaluacion_Equipo_Usuario para la base de datos
Fields:
    id_Evaluacion   : (UUID) Identificador de la evaluación en curso
    id_Equipo       : (UUID) Identificador del equipo evaluado
    id_Usuario      : (Char) Identificador del evaluador (email)
    puntajes        : (Char) Puntajes asignados al equipo por el usuario en la evaluacion
Author:
Nicolás Machuca
"""
# class Evaluacion_Equipo_Usuario(models.Model):
#     id_Evaluación = models.ForeignKey('Evaluacion.Evaluacion',  on_delete=models.CASCADE, blank=False, null=False)
#     id_Equipo     = models.ForeignKey('Equipo.Equipo', on_delete=models.CASCADE, blank=False, null=False)
#     id_Usuario    = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
#     puntajes      = models.CharField(blank=False, default='[]', max_length = 120)

#     def get_puntajes(self):
#         return json.loads(self.puntajes)
    
#     def set_puntajes(self, list):
#         self.puntajes = json.dumps(list)