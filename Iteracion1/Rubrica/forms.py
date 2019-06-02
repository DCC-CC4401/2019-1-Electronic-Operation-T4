from django import forms
from .models import Rubrica

class CreateForm(forms.Form):
     nombre = forms.CharField(widget=forms.TextInput(attrs={
          'placeholder':'Nombre de la Rubrica',
          'name':'nombre_rubrica',
          'id':'nombre-rubrica',
          'class':'w3-input w3-border w3-margin-bottom'
     }),max_length=100)
     rubrica = forms.FileField(widget=forms.ClearableFileInput({
          'name':'archivo-rubrica',
          'id':'archivo'
     }))
     tiempoMin = forms.TimeField(widget=forms.TextInput(
          attrs= {
               'placeholder':'HH:MM',
               'name':'tiempo_min',
               'id':'tiempo-min',
               'class':' w3-border w3-margin-bottom'
          }
     ))
     tiempoMax = forms.TimeField(widget=forms.TextInput(
          attrs= {
               'placeholder':'HH:MM',
               'name':'tiempo_max',
               'id':'tiempo-max',
               'class':' w3-border w3-margin-bottom'
          }
     ))