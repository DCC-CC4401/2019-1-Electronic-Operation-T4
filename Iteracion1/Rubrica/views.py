from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from .models import Rubrica

class RubricaListView(ListView):
     template_name = 'Admin-landing/admin_rubricas_gestion.html'
     queryset = Rubrica.objects.all()