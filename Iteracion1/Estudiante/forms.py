from django import forms

from .models import Estudiante

""" Formulario para la creación de un estudiante
Fields:
    id_Equipo   : (UUID) Referencia al equipo al que pertenece el estudiante
    historial   : (File) Archivo que contiene los equipos de los que ha formado parte el estudiante 
    Nombre      : (String) Nombre del estudiante
    Notas       : (File) Archivo con las notas del alumno
Author:
    Clemente Paredes
"""

class CreacionEstudiante(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['id_Equipo', 'historial', 'Nombre', 'Notas']  #Cambiar a nombre de equipo?
                                                                #Generar historial y Notas automáticamente

""" Formulario para cambio de equipo
Fields:
    id              : (UUID) Identificador del registro
    id_Equipo       : (UUID) Referencia al nuevo equipo al que pertenece el estudiante
    nombre_Equipo   : (String) Nombre del equipo nuevo equipo al que pertenece el estudiante
Author:
    Clemente Paredes
"""

class CambioEquipo(forms.ModelForm):
    nombre_Equipo = forms.CharField(max_length=2000)
    class Meta:
        model = Estudiante
        fields = ['id', 'id_Equipo', 'nombre_Equipo']

""" Formulario para actualización de notas
Fields:
    id          : (UUID) Identificador del registro
    Notas       : (File) Archivo con las notas del alumno
Author:
    Clemente Paredes
"""

class ActualizarNotas(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['id', 'Notas'] #Permitir ingresar notas como Float?