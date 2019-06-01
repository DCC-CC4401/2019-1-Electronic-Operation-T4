from django import forms
from django.forms import ModelForm
from django.db.utils import OperationalError
from .models import Usuario_Evaluacion, Evaluacion_Rubrica


class FormUsuarioEnEvaluacion(forms.Form):
    evaluador = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple({
                'name': 'select-evaluadores',
                'id' : 'select_evaluador'
            }))
    def __init__(self,*args,**kwargs):
        id_evaluacion = kwargs.pop('id_evaluacion')
        super(FormUsuarioEnEvaluacion, self).__init__(*args,**kwargs)
        try:
            usuarios_evaluando = Usuario_Evaluacion.objects.filter(id_Evaluación=id_evaluacion)
            correos = ((x.id_Usuario.correo_Electrónico) for x in usuarios_evaluando)
            users = Usuario.objects.all().exclude(correo_Electrónico__in=correos)
            self.fields['evaluador'].choices = ((x.id, x.nombre + " " + x.apellido) for x in users)
        except OperationalError:
            self.fields['evaluador'].choices = []
    
class EvaluacionRubricaForm(ModelForm):
    class Meta:
        model  = Evaluacion_Rubrica
        fields = ['id_Evaluacion', 'id_Rúbrica']