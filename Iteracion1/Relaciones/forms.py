from django import forms
from Usuario.models import Usuario
from django.db.utils import OperationalError
from .models import Usuario_Evaluacion


class FormUsuarioEnEvaluacion(forms.Form):
    # def __init__(self,*args,**kwargs):
    #     id_evaluacion = kwargs.pop('id_evaluacion')
    #     super(FormUsuarioEnEvaluacion, self).__init__(*args,**kwargs)
    #     self.fields['usuarios_evaluando'].filter(id_Evaluación=id_evaluacion)
    try:
        #usuarios_evaluando = Usuario_Evaluacion.objects.all()
        #correos = ((x.id_Usuario.correo_Electrónico) for x in usuarios_evaluando)
        users = Usuario.objects.all()
        
        evaluador = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple({
            'name': 'select-evaluadores',
            'id' : 'select_evaluador'
        }), choices=((x.id, str(x.nombre) + " " + str(x.apellido)) for x in users))
    except OperationalError:
        evaluador = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple({
            'name': 'select-evaluadores',
            'id' : 'select_evaluador'
        }))
    
    