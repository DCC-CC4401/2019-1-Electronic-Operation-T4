from django.shortcuts import render

# Create your views here.
def home_view(request,*args,**kwargs):
     return render(request,"base.html",{})
def landing_evaluaciones_view(request,*args,**kwargs):
     return render(request,"Admin-landing/admin_evaluaciones_gestion.html",{})
def ficha_rubrica_admin_view(request,*args,**kwargs):
     return render(request,"Ficha-rubricas/ficha_rubrica_admin.html",{})

def ficha_rubrica_evaluador_view(requesr, *arg, **kwargs):
     return render(request, "Fichas-rubricas/ficha_rubrica_evaluador.html", {})
def landing_evaluadores_view(request, *arg, **kwargs):
     return render(request, "Admin-landing/admin_evaluadores_gestion.html", {})
def landing_rubricas_view(request, *arg, **kwargs):
     return render(request, "Admin-landing/admin_rubricas_gestion.html", {})
def ficha_evaluacion_admin_view(request, *arg, **kwargs):
     return render(request, "Ficha-evaluaciones/ficha_evaluacion_admin.html", {})
def admin_rubricas_gestion_view(request):
     return render(request,"Admin-landing/admin_rubricas_gestion.html",{})