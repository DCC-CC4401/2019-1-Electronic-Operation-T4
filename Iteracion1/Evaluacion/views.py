import csv
import os
import subprocess
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from Evaluacion.models import Evaluacion
from Curso.models import Curso 
from Rubrica.models import Rubrica




class EvaluacionListView(ListView):
    template_name = 'Evaluadores-landing/evaluadores-landing.html'
    eval_details = Evaluacion.objects.all().order_by('-fecha_Inicio')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

def evaluacion_view(request, rubrica_id):
    rubrica = get_object_or_404(Rubrica, id=rubrica_id)
    #curso = get_object_or_404(Curso, id=curso_id)
    # evaluacion = get_object_or_404(Evaluacion, id=eval_id)
    context = dict()
    #context["curso"] = curso
    #context["evaluacion"] = evaluacion
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
               context['nombre']  = rubrica.nombre
               context['rubrica'] = data_rubrica
               context['max_length'] = max_length 
               context['duracion_min'] = my_rubrica.duración_Mínima
               context['duracion_max'] = my_rubrica.duración_Máxima
    except FileNotFoundError:
          raise Http404('No se pudo encontrar el archivo de rubrica')
    
    return render(request,'Ficha-evaluaciones/ficha_evaluacion_admin.html',context)
    


    






