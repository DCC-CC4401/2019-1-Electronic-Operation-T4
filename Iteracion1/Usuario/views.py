from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegistroUsuarioForm

# Create your views here.

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

def login(request,*arg, **kwargs):
    return
#    if request.method == 'POST':          
#          form = AuthenticationForm(request.POST)
#          if form.is_valid():       
#    else:
#          form= AuthenticationForm()
#     return render(request)