import csv
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,Http404
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import Rubrica

class RubricaListView(ListView):
     template_name = 'Admin-landing/admin_rubricas_gestion.html'
     queryset = Rubrica.objects.all()

def rubrica_detail_view(request,rubrica_id):
     my_rubrica = get_object_or_404(Rubrica,id=rubrica_id)
     rubrica_path = my_rubrica.rúbrica.path
     context_data = dict()
     try:
          with open(rubrica_path,newline='') as my_file:
               reader = csv.reader(my_file,delimiter=',')
               data_rubrica = list()
               max_length = 0
               for row in reader:
                    columna = list()
                    for dato in row:
                         columna.append(dato)
                    data_rubrica.append(columna)
                    if max_length < len(columna):
                         max_length = len(columna)
               context_data['nombre']  = my_rubrica.nombre
               context_data['rubrica'] = data_rubrica
               context_data['max_length'] = max_length 
               context_data['duracion_min'] = my_rubrica.duración_Mínima
               context_data['duracion_max'] = my_rubrica.duración_Máxima
               return render(request,'Ficha-rubricas/detalles_rubrica.html',context_data)
     except FileNotFoundError:
          raise Http404('No se pudo encontrar el archivo de rubrica')
     

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

          
