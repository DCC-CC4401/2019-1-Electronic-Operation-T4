from django.forms import ModelForm
from django import forms

from Relaciones.models import Evaluacion_Curso, Evaluacion_Rubrica
from Curso.models import Curso
from Rubrica.models import Rubrica
from Evaluacion.models import Evaluacion
from django.contrib.auth.models import User
from Nombre_Curso.models import Nombre_Curso
from django.db.utils import OperationalError
from .models import Evaluacion
from Relaciones.models import Usuario_Evaluacion

class ActualizarPlazoForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['fecha_Inicio', 'fecha_Fin']

"""
@deprecated
"""
class CreateFormEvaluacion(forms.Form):
    def __init__(self,*args,**kwargs):
        super(CreateFormEvaluacion, self).__init__(*args,**kwargs)
        try:
            nombre_cursos = Nombre_Curso.objects.all()
            self.fields['curso'].choices = ((x.id_Curso.id, str(x.id_Curso.código) + "-" +
                                        str(x.id_Curso.número_sección) + " " +
                                        str(x.Nombre) + " " +
                                        str(x.id_Curso.año) + "-" +
                                        str(x.id_Curso.semestre)) for x in nombre_cursos)
            rubrica_select = Rubrica.objects.all()
            self.fields['rubrica'].choices = ((x.id, x.nombre ) for x in rubrica_select)
        except OperationalError:
            self.fields['nombre_cursos'].choices = []
            self.fields['rubrica'].choices = []
    nombre = forms.CharField(widget=forms.TextInput(attrs={
          'placeholder':'Nombre de la Evaluacion',
          'name':'nombre_evaluacion',
          'id':'nombre-evaluacion',
          'class':'w3-input w3-border w3-margin-bottom'

     }),max_length=100) 

    fecha_inicio = forms.DateField(widget=forms.DateInput({
        'name':'fecha_inicio',
        'id':'fecha-inicio',
        'type': 'Date'
    }))

    fecha_fin = forms.DateField(widget=forms.DateInput({
        'name':'fecha_fin',
        'id':'fecha-fin',
        'type': 'Date'
    }))
    curso = forms.ChoiceField(widget=forms.Select({
        'name':'curso-evaluacion',
        'id':'curso'
    }))
    
    rubrica = forms.ChoiceField(widget=forms.Select({
        'name':'rubrica-evaluacion',
        'id':'rubrica'
    }))

"""
@deprecated
"""
class FormSelectRubrica(forms.Form):
    def __init__(self,*args,**kwargs):
        super(FormSelectRubrica, self).__init__(*args,**kwargs)
        try:
            rubrica_select = Rubrica.objects.all()
            self.fields['rubrica'].choices = ((x.id, x.nombre ) for x in rubrica_select)
        except OperationalError:
            self.fields['rubrica'].choices = []
            rubrica = forms.ChoiceField(widget=forms.Select({
            'name':'rubrica-evaluacion',
            'id':'rubrica'
        }))


"""
Formulario para la creacion de evaluaciones
Fields:
    nombre          :   Nombre de la evaluacion.
    fecha_Inicio    :   Fecha de inicio de la evaluacion
    fecha_Fin       :   Fecha de termino de la evaluacion

Author:
    Nicolás Machuca
"""
class CreateEvaluacion(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['nombre', 'fecha_Inicio', 'fecha_Fin', 'id_Curso']
        widgets = {
            'fecha_Inicio' : forms.DateInput({
                'id':'fecha-inicio',
                'name': 'mod_fecha_inicio',
                'type': 'Date'
            }),
            'fecha_Fin' : forms.DateInput({
                'name' : 'mod_fecha_fin',
                'id':'fecha-fin',
                'type': 'Date'
            }),
            'nombre'    : forms.TextInput({
                'id' : 'nombre',
                'name': 'mod_nombre'
            })
            }
        labels = {
            "id_Curso": "Curso"
        }
        

"""
Formulario para asociar una rubrica a una evaluacion.
Fields:
    id_Evaluación   :   Referencia a la evaluacion asociada.
    id_Rúbrica      :   Referencia a la rubrica que usa la evaluacion asociada.

Author:
    Nicolás Machuca
"""
class CreateRubricaEvaluacion(ModelForm):
    class Meta:
        model = Evaluacion_Rubrica
        fields = ['id_Rúbrica', 'id_Evaluación']
        labels= {
            "id_Rúbrica": "Rúbrica"
        }


"""
Formulario para cambiar la rubrica asociada a una evaluacion

"""
class UpdateRubricaEvaluacion(ModelForm):
    class Meta:
        model = Evaluacion_Rubrica
        fields = ['id_Rúbrica']
        labels= {
            "id_Rúbrica": "Rúbrica"
        }


class ActualizarPlazoForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['fecha_Inicio', 'fecha_Fin']

"""
Formulario para asociar un curso a una evaluacion.
Fields:
    id_Evaluación   :   Referencia a la evaluacion asociada.
    id_Curso        :   Referencia al curso que se esta evaluando.

Author:
    Nicolás Machuca
"""
class CreateCursoEvaluacion(ModelForm):
    class Meta:
        model = Evaluacion_Curso
        fields = ['id_Curso', 'id_Evaluación']
