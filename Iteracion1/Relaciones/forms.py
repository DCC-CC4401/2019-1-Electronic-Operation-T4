from django import forms
from Usuario.models import Usuario
from django.db.utils import OperationalError
from .models import Usuario_Evaluacion

"""
Formulario para agregar evaluadores a una evaluacion


TODO: Revisar si se puede cambiar por modelForm
"""
class FormUsuarioEnEvaluacion(forms.Form):
    evaluadores = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple({
                'name': 'select-evaluadores',
                'id' : 'select_evaluador',
                'class' :'w3-ul w3-border'
            }), required=False)
    def __init__(self,*args,**kwargs):
        id_evaluacion = kwargs.pop('id_evaluacion')
        super(FormUsuarioEnEvaluacion, self).__init__(*args,**kwargs)
        try:
            usuarios_evaluando = Usuario_Evaluacion.objects.filter(id_Evaluación=id_evaluacion)
            correos = ((x.id_Usuario.correo_Electrónico) for x in usuarios_evaluando)
            users = Usuario.objects.all().exclude(correo_Electrónico__in=correos)
            self.fields['evaluadores'].choices = ((x.id, x.nombre + " " + x.apellido) for x in users)
        except OperationalError:
            self.fields['evaluadores'].choices = []


class FormAgregarPresentador(forms.Form):
    presentadores = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple({
                'name': 'select-presentador',
                'id' : 'select_presentador',
                'class' :'w3-ul w3-border'
            }), required=False)
    def __init__(self,*args,**kwargs):
        evaluacion = kwargs.pop('evaluacion')
        equipo = kwargs.pop('equipo')
        super(FormAgregarPresentador, self).__init__(*args,**kwargs)
        try:
            estudiantes_presentando = Evaluacion_Estudiante.objects.filter(id_Evaluación=evaluacion)

            ids = ((x.id_Estudiante.id) for x in estudiantes_presentando)
            students = Estudiante.objects.filter(id_Equipo=equipo).exclude(id__in=ids)
            self.fields['presentadores'].choices = ((x.id, x.Nombre) for x in students)
        except OperationalError:
            self.fields['presentadores'].choices = []
    
    