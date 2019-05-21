import csv
import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from Evaluacion.models import Evaluacion
from Relaciones.models import Evaluacion_Curso, Evaluacion_Rubrica, Usuario_Evaluacion, Evaluacion_Equipo
from Curso.models import Curso 
from Rubrica.models import Rubrica
from Equipo.models import Equipo
from django.http import JsonResponse, Http404, HttpResponse
from .forms import CreateFormEvaluacion
from Relaciones.forms import FormUsuarioEnEvaluacion




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
               nombre_evaluacion = form.cleaned_data.get("nombre")
               fecha_inicio = form.cleaned_data.get("fecha_inicio")
               fecha_fin = form.cleaned_data.get("fecha_fin")
               rubrica_id = form.cleaned_data.get("rubrica")
               curso = form.cleaned_data.get("curso")
               curso_obj = Curso.objects.get(id=curso)
               rubrica_obj = Rubrica.objects.get(id=rubrica_id)
               e = Evaluacion.objects.create(nombre=nombre_evaluacion, fecha_Inicio=fecha_inicio, fecha_Fin=fecha_fin, is_Open=True)
               eval_obj = Evaluacion.objects.get(id = e.id)
               Evaluacion_Curso.objects.create(id_Curso=curso_obj, id_Evaluacion=eval_obj)
               Evaluacion_Rubrica.objects.create(id_Evaluacion=eval_obj, id_Rúbrica=rubrica_obj)
               message.append('Evaluacion creada con exito!')
     form = CreateFormEvaluacion()
     obj = Evaluacion.objects.all().order_by('-fecha_Inicio')
     context = {'object_list':obj,'form':form,'mensaje':message}
     return render(request,'Admin-landing/admin_evaluaciones_gestion2.html',context)

def evaluacion_view(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
    rubrica_evaluacion = get_object_or_404(Evaluacion_Rubrica, id_Evaluacion=evaluacion_id)
    curso_evaluacion = get_object_or_404(Evaluacion_Curso, id_Evaluacion=evaluacion_id)
    rubrica = get_object_or_404(Rubrica, id=rubrica_evaluacion.id_Rúbrica.id)
    rubrica_path = rubrica.rúbrica.path
    curso = get_object_or_404(Curso, id=curso_evaluacion.id_Curso.id)

    evaluados = Evaluacion_Equipo.objects.filter(id_Evaluación=evaluacion)
    
    lista_evaluados = ((x.id_Equipo.id) for x in evaluados)
    equipos = Equipo.objects.filter(id_Curso=curso).exclude(id__in=lista_evaluados)

    
    # evaluacion = get_object_or_404(Evaluacion, id=eval_id)
    context = dict()
    context["curso"] = curso
    context["evaluacion"] = evaluacion
    context["equipos"] = equipos
    if curso.semestre == 1:
         context["semestre"] = "Otoño"
    elif curso.semestre == 2:
         context["semestre"] = "Primavera"
    
    else:
         context["semestre"] = "Verano"
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
               context['nombre_rubrica']  = rubrica.nombre
               context['rubrica'] = data_rubrica
               context['max_length'] = max_length 
               context['duracion_min'] = rubrica.duración_Mínima
               context['duracion_max'] = rubrica.duración_Máxima
    except FileNotFoundError:
          raise Http404('No se pudo encontrar el archivo de rubrica asociada')
    return render(request,'Ficha-evaluaciones/ficha_evaluacion_admin.html',context)

def evaluacion_delete_view(request, evaluacion_id):
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
    
def get_evaluadores(request):
     my_id = request.GET.get('query_id')
     id_evaluacion = Evaluacion.objects.get(id=my_id)
     form = FormUsuarioEnEvaluacion()
     data=dict()
     print('---------------', form.as_table())
     data['form'] = form.as_table()
     return JsonResponse(data)


from .forms import ActualizarPlazoForm

# Create your views here.

def actualizarPlazo(request, *args, **kwargs):
    if request.method == 'POST':
        form = ActualizarPlazoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ActualizarPlazoForm()
    for key, value in kwargs.items():
        if key == 'path':
            path = value
    return render(request, path, {'form' : form})
    #Implementar en conjunto con frontend
