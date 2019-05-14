from django.forms import ModelForm

from .models import Evaluacion

class ActualizarPlazoForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['fecha_Inicio', 'fecha_Fin']