import csv
import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from Evaluacion.models import Evaluacion
from Relaciones.models import Evaluacion_Curso, Evaluacion_Rubrica
from Curso.models import Curso 
from Rubrica.models import Rubrica
from django.http import JsonResponse, Http404
from .forms import CreateFormEvaluacion




class EvaluacionListView(ListView):
    template_name = 'Evaluadores-landing/evaluadores-landing.html'
    eval_details = Evaluacion.objects.all().order_by('-fecha_Inicio')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
def evaluacion_list_and_create(request):
     message = []
     if request.method == 'POST':
          form = CreateFormEvaluacion(request.POST)
          if form.is_valid():
               nombre = form.cleaned_data.get("nombre")
               fecha_inicio = form.cleaned_data.get("fecha_inicio")
               fecha_fin = form.cleaned_data.get("fecha_fin")
               rubrica_id = form.cleaned_data.get("rubrica")
               curso = form.cleaned_data.get("curso")
               curso_obj = Curso.objects.get(id=curso)
               rubrica_obj = Rubrica.objects.get(id=rubrica_id)
               e = Evaluacion.objects.create(nombre=nombre, fecha_Inicio=fecha_inicio, fecha_Fin=fecha_fin, is_Open=True)
               eval_obj = Evaluacion.objects.get(id = e.id)
               Evaluacion_Curso.objects.create(id_Curso=curso_obj, id_Evaluacion=eval_obj)
               Evaluacion_Rubrica.objects.create(id_Evaluacion=eval_obj, id_Rúbrica=rubrica_obj)
               message.append('Evaluacion creada con exito!')
     form = CreateFormEvaluacion()
     obj = Evaluacion.objects.all().order_by('-fecha_Inicio')
     context = {'object_list':obj,'form':form,'mensaje':message}
     return render(request,'Admin-landing/admin_evaluaciones_gestion2.html',context)

def evaluacion_view(request, rubrica_id):
    rubrica = get_object_or_404(Rubrica, id=rubrica_id)
    rubrica_path = rubrica.rúbrica.path
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
               context['duracion_min'] = rubrica.duración_Mínima
               context['duracion_max'] = rubrica.duración_Máxima
    except FileNotFoundError:
          raise Http404('No se pudo encontrar el archivo de rubrica')
    
    return render(request,'Ficha-evaluaciones/ficha_evaluacion_admin.html',context)
def evaluacion_delete_view(request):
     if request.method == "POST":
          obj = Evaluacion.objects.get(id=evaluacion_id)
          obj.delete()
     return redirect("resumen-evaluaciones", permanent=True)

def getting_details_evaluaciones_view(request):
     my_id = request.GET.get('query_id')
     obj = Evaluacion.objects.get(id=my_id)
     data=dict()
     data['Fecha de inicio: '] = obj.fecha_Inicio
     data['Fecha fin: '] = obj.fecha_Fin
     data['Estado: '] = obj.is_Open

     return JsonResponse(data)
    


    






