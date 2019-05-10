from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

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
     contraseña = ""
     if request.method == 'POST':          
          form = RegistroUsuarioForm(request.POST)
          if form.is_valid():       
               usuario = form.save(commit=False)
               contraseña = "Tu contraseña es: " + User.objects.make_random_password()
               usuario.set_password(contraseña)
               usuario.username = usuario.email
               usuario.save()
     else:
          form = RegistroUsuarioForm()
     for key, value in kwargs.items():
          if key == 'path':
               path = value
     return render(request, path, {'form' : form, 'contraseña' : contraseña})

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
                print(usuario)
                login(request, usuario)
                return HttpResponseRedirect('landing1/')
            else:
                print('Usuario no encontrado')
    else:
          form= AuthenticationForm()

    for key, value in kwargs.items():
          if key == 'path':
               path = value
    return render(request, path, {'form':form})
