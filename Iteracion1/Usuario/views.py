from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistroUsuarioForm

# Create your views here.

def registro(request, *arg, **kwargs):
     if request.method == 'POST':          
          form = RegistroUsuarioForm(request.POST)
          if form.is_valid():
               #username = email o guardar en modelo Usuario              
               form.save()
               NombreUsuario=form.cleaned_data.get('email')
     else:
          form = RegistroUsuarioForm()
     for key, value in kwargs.items():
          if key == 'path':
               path = value
     return render(request, path, {'form' : form})