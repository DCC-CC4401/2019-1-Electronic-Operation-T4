from django.shortcuts import render

# Create your views here.
def home_view(request,*args,**kwargs):
     return render(request,"base.html",{})
def landing_evaluaciones_view(request,*args,**kwargs):
     return render(request,"Admin-landing/admin_evaluaciones_gestion.html",{})