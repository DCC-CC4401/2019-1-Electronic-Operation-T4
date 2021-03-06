from django.shortcuts import render
from Usuario.views import registro as rg
from Usuario.views import login_view as lg
from django.contrib.auth.decorators import login_required
from Evaluacion.views import evaluacion_list_and_create, crearEvaluacion, evaluacion_list_evaluador
from Rubrica.views import rubrica_list_and_create
from Usuario.views import evaluador_list_and_create
from django.contrib.auth import logout


# Create your views here.
@login_required(login_url="/login/")
def home_view(request,*args,**kwargs):
     if(request.user.is_superuser):
          return render(request,"Usuario/landing.html",{})
     else:
          return render(request,"Usuario/landing_evaluador.html",{})

def logout_view(request):
     logout(request)
     return lg(request, path='Usuario/ingreso.html')

@login_required(login_url="/login/")
def landing_evaluaciones_view(request,*args,**kwargs):
     if(request.user.is_superuser):
          return evaluacion_list_and_create(request)
          
     else:
          return evaluacion_list_evaluador(request)

@login_required(login_url="/login/")     
def landing_evaluadores_view(request, *arg, **kwargs):
          return evaluador_list_and_create(request)

@login_required(login_url="/login/")
def landing_rubricas_view(request, *arg, **kwargs):
          return rubrica_list_and_create(request)
     

@login_required(login_url="/login/")
def ficha_rubrica_view(request,*args,**kwargs):
     if(request.user.is_superuser):
          return render(request,"Ficha-rubricas/ficha_rubrica_admin.html",{})
     else:
          return render(request, "Ficha-rubricas/ficha_rubrica_evaluador.html", {})

@login_required(login_url="/login/")
def ficha_evaluacion_admin_view(request, *arg, **kwargs):
     return render(request, "Ficha-evaluaciones/ficha_evaluacion_admin.html", {})

@login_required(login_url="/login/")
def registro(request, *args, **kwargs):
     return rg(request, path='Usuario/registro.html')


def login(request, *args, **kwargs):
     return lg(request, path='Usuario/ingreso.html')

def evaluacion_prueba(request, *args, **kwargs):
     return crearEvaluacion(request, path='Ficha-evaluaciones/ficha_evaluacion_admin_prueba.html')



""" 
Comento esto por si ocurre un error en el refactoring


def home_view(request,*args,**kwargs):
     return render(request,"base.html",{})

@login_required(login_url="/login/")
def landing_evaluaciones_view(request,*args,**kwargs):
          return render(request,"Admin-landing/admin_evaluaciones_gestion.html",{})

@login_required(login_url="/login/")     
     return render(request,"Admin-landing/admin_evaluaciones_gestion2.html",{})
def ficha_rubrica_admin_view(request,*args,**kwargs):
     return render(request,"Ficha-rubricas/ficha_rubrica_admin.html",{})

def ficha_rubrica_evaluador_view(request, *arg, **kwargs):
     return render(request, "Fichas-rubricas/ficha_rubrica_evaluador.html", {})
def landing_evaluadores_view(request, *arg, **kwargs):
     return render(request, "Admin-landing/admin_evaluadores_gestion.html", {})

@login_required(login_url="/login/")
def landing_rubricas_view(request, *arg, **kwargs):
     return render(request, "Admin-landing/admin_rubricas_gestion.html", {})

@login_required(login_url="/login/")
def admin_rubricas_gestion_view(request):
     return render(request,"Admin-landing/admin_rubricas_gestion.html",{})



@login_required(login_url="/login/")
def ficha_rubrica_admin_view(request,*args,**kwargs):
     
     return render(request,"Ficha-rubricas/ficha_rubrica_admin.html",{})

@login_required(login_url="/login/")
def ficha_rubrica_evaluador_view(request, *arg, **kwargs):
     return render(request, "Ficha-rubricas/ficha_rubrica_evaluador.html", {})

@login_required(login_url="/login/")
def ficha_evaluacion_admin_view(request, *arg, **kwargs):
     return render(request, "Ficha-evaluaciones/ficha_evaluacion_admin.html", {})


def registro(request, *args, **kwargs):
     return rg(request, path='Usuario/registro.html')


def login(request, *args, **kwargs):
     return lg(request, path='Usuario/ingreso.html')
"""