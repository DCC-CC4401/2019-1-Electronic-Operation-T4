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

class CrearEvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['nombre', 'fecha_Inicio', 'fecha_Fin']

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
            curso = forms.ChoiceField(widget=forms.Select({
                'name':'curso-evaluacion',
                'id':'curso'
            }))
    
"""class AgregarEvaluadorForm(forms.Form):
    try:
        evaluaciones = Evaluacion.objects.all()
        evaluacion = forms.ChoiceField(widget=forms.Select({
            'name'  : 'Evaluación',
            'id'    : 'evaluacion'
        }),
        choices=((x.id, str(x.nombre)) for x in evaluaciones))
        evaluadores = User.objects.all()
        evaluador = forms.ChoiceField(widget=forms.Select({
            'name'  : 'Evaluador',
            'id'    : 'evaluador'
        }),
        choices=((x.username, str(x.username)) for x in evaluadores))
    except OperationalError:
        evaluación = forms.ChoiceField(widget=forms.Select({
            'name'  : 'Evaluación',
            'id'    : 'evaluacion'
        })),
        evaluador = forms.ChoiceField(widget=forms.Select({
            'name'  : 'Evaluador',
            'id'    : 'evaluador'
        }))"""
