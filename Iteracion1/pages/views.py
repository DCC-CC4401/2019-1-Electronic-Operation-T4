from django.shortcuts import render
from Usuario.views import registro as rg


from django.contrib.auth.forms import UserCreationForm
from Usuario.forms import RegistroUsuarioForm
# Create your views here.
def home_view(request,*args,**kwargs):
     return render(request,"base.html",{})

def landing_evaluaciones_view(request,*args,**kwargs):
     return render(request,"Admin-landing/admin_evaluaciones_gestion.html",{})
def landing_evaluadores_view(request, *arg, **kwargs):
     return render(request, "Admin-landing/admin_evaluadores_gestion.html", {})
def landing_rubricas_view(request, *arg, **kwargs):
     return render(request, "Admin-landing/admin_rubricas_gestion.html", {})
def admin_rubricas_gestion_view(request):
     return render(request,"Admin-landing/admin_rubricas_gestion.html",{})

def ficha_rubrica_admin_view(request,*args,**kwargs):
     return render(request,"Ficha-rubricas/ficha_rubrica_admin.html",{})
def ficha_rubrica_evaluador_view(request, *arg, **kwargs):
     return render(request, "Ficha-rubricas/ficha_rubrica_evaluador.html", {})

def ficha_evaluacion_admin_view(request, *arg, **kwargs):
     return render(request, "Ficha-evaluaciones/ficha_evaluacion_admin.html", {})

def registro(request, *args, **kwargs):
     return rg(request, path='Usuario/registro.html')
     
def registro(request, *arg, **kwargs):
     if request.method == 'POST':
          
          form = RegistroUsuarioForm(request.POST)
          if form.is_valid():
               
               form.save()
               NombreUsuario=form.cleaned_data.get('username')
     else:
          form = RegistroUsuarioForm()
     return render(request, "Usuario/registro.html", {'form' : form})
