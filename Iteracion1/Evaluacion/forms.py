from django import forms
from Relaciones.models import Evaluacion_Curso, Evaluacion_Rubrica
from Curso.models import Curso
from Rubrica.models import Rubrica
from Nombre_Curso.models import Nombre_Curso
from django.db.utils import OperationalError


class CreateFormEvaluacion(forms.Form):
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
    try:
        nombre_cursos = Nombre_Curso.objects.all()
        curso = forms.ChoiceField(widget=forms.Select({
            'name':'curso-evaluacion',
            'id':'curso'
        }), choices=((x.id_Curso.id, str(x.id_Curso.código) + "-" +
                                        str(x.id_Curso.número_sección) + " " +
                                        str(x.Nombre) + " " +
                                        str(x.id_Curso.año) + "-" +
                                        str(x.id_Curso.semestre)) for x in nombre_cursos))
        rubrica_select = Rubrica.objects.all()
        rubrica = forms.ChoiceField(widget=forms.Select({
            'name':'rubrica-evaluacion',
            'id':'rubrica'
        }), choices=((x.id, x.nombre ) for x in rubrica_select))
    except OperationalError:
        rubrica = forms.ChoiceField(widget=forms.Select({
            'name':'rubrica-evaluacion',
            'id':'rubrica'
        }))
        curso = forms.ChoiceField(widget=forms.Select({
            'name':'curso-evaluacion',
            'id':'curso'
        }))
    
