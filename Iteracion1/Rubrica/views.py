import csv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
# Create your views here.
from .models import Rubrica

class RubricaListView(ListView):
     template_name = 'Admin-landing/admin_rubricas_gestion.html'
     queryset = Rubrica.objects.all()

def getting_aspects_view(request):
     my_id = request.GET.get('query_id')
     obj = Rubrica.objects.get(id=my_id)
     data = dict()
     with open(obj.rúbrica.path,newline='') as my_file:
          reader = csv.reader(my_file,delimiter=',')
          count = 0
          for row in reader:
               if count!=0:
                    data[f'Aspecto{count}']=row[0]
               count+=1
     return JsonResponse(data)

          
