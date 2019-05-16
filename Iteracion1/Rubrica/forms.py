from django import forms
from .models import Rubrica

class UpdateForm(forms.Form):
     
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