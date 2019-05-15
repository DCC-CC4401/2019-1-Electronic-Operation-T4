from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserModel


from .models import Usuario
class RegistroUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
