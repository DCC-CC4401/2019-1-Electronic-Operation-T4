from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages

from .forms import RegistroUsuarioForm, ModificarUsuarioForm

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


def evaluador_list_and_create(request, *arg, **kwargs):
     texto = ""
     path = 'Admin-landing/admin_evaluadores_gestion.html'
     usuarios = User.objects.all()
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
                return render(request, path, {'object_list' : usuarios, 'form' : form, 'contraseña': "", 'error' : error})
     else:
          form = RegistroUsuarioForm()    
     if(request.user.is_superuser):
        return render(request, path, {'object_list' : usuarios, 'form' : form, 'contraseña' : texto, 'error' : ""})
     



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
                return HttpResponseRedirect('..')
    else:
          form= AuthenticationForm()
    for key, value in kwargs.items():
        if key == 'path':
            path = value
    return render(request, path, {'form' : form})

@staff_member_required
def usuario_delete_view(request, username):
    if request.method == 'POST':
        try:
            obj = User.objects.get(username=username)
            obj.delete()
            massages.success(request, "Usuario eliminado")
            return HttpResponseRedirect('..')
        except User.DoesNotExist:
            messages.error(request, "Usuario no encontrado")
            return HttpResponseRedirect('..')
        except Exception as e:
            messages.error(request, e.message)
            return HttpResponseRedirect('..')
    else:
        return HttpResponseRedirect('..')

@staff_member_required
def usuario_modificar_view(request, username):
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            try:
                obj = User.objects.get(username=username)
                obj.first_name = respuesta.first_name
                obj.last_name = respuesta.last_name
                obj.save()
            except User.DoesNotExist:
                messages.error(request, "Usuario no encontrado")
                return HttpResponseRedirect('..')
            except Exception as e:
                messages.error(request, e.message)
                return HttpResponseRedirect('..')
            return HttpResponseRedirect('..')
    else:
        form = ModificarUsuarioForm()
        path = "Usuario/modificar_evaluador.html"
        return render(request, path, {'form' : form, 'nombre': username})