from django.shortcuts import render
from Usuario.views import registro as rg
from Usuario.views import login_view as lg
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_view(request,*args,**kwargs):
     return render(request,"base.html",{})

@login_required(login_url="/login/")
def landing_evaluaciones_view(request,*args,**kwargs):
     return render(request,"Admin-landing/admin_evaluaciones_gestion.html",{})

@login_required(login_url="/login/")     
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
