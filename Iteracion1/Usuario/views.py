from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import IntegrityError

from .forms import RegistroUsuarioForm

# Create your views here.

""" Registra un nuevo usuario en la base de datos.
Args:
    request : (HttpRequest) Request del navegador.
    path    : (String) Ubicación de la página de registro.
Raises:
    IntegrityError : Al intentar crear un usuario que ya está en la base de datos.
Returns:
    (HttpResponse) Render de la página de registro.
"""
def registro(request, *arg, **kwargs):
     for key, value in kwargs.items():
          if key == 'path':
               path = value
     texto = ""
     if request.method == 'POST':          
          form = RegistroUsuarioForm(request.POST)
          if form.is_valid():
              try:    
               usuario = form.save(commit=False)
               contraseña= User.objects.make_random_password()
               texto = "Tu contraseña es: " + contraseña
               usuario.set_password(contraseña)
               usuario.username = usuario.email
               usuario.save()
              except IntegrityError:
                error = "Este usuario ya existe"
                return render(request, path, {'form' : form, 'contraseña': "", 'error' : error})
     else:
          form = RegistroUsuarioForm()
     return render(request, path, {'form' : form, 'contraseña' : texto, 'error' : ""})

""" Autentica un usuario existente.
Args:
    request : (HttpRequest) Request del navegador.
    path    : (String) Ubicación de la página de login.
Returns:
    (HttpResponse) Render de la página de landing si es correcto, 
                    render de la página de login si no lo es.
"""
def login_view(request,*arg, **kwargs):
    if request.method == 'POST':          
          form = AuthenticationForm(request=request, data=request.POST)
          if form.is_valid():
            
            username = form.cleaned_data.get('username')
            contraseña = form.cleaned_data.get('password')
            usuario = authenticate(username=username, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                return HttpResponseRedirect('landing1/')
    else:
          form= AuthenticationForm()
    for key, value in kwargs.items():
        if key == 'path':
            path = value
    return render(request, path, {'form' : form})
