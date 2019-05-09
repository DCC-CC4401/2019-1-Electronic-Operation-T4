from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserModel

from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):

    
    class Meta:
        model = User
        fields  = ['email','first_name', 'last_name']