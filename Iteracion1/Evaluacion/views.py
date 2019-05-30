import csv
import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from Evaluacion.models import Evaluacion
from Relaciones.models import Evaluacion_Curso, Evaluacion_Rubrica, Usuario_Evaluacion, Evaluacion_Equipo
from Curso.models import Curso 
from Estudiante.models import Estudiante
from Rubrica.models import Rubrica
from Equipo.models import Equipo
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404, HttpResponse
from .forms import CreateFormEvaluacion, FormSelectRubrica
from Relaciones.forms import FormUsuarioEnEvaluacion
from django.core.cache import cache




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
               Evaluacion_Curso.objects.create(id_Curso=curso_obj, id_Evaluación=eval_obj)
               Evaluacion_Rubrica.objects.create(id_Evaluación=eval_obj, id_Rúbrica=rubrica_obj)
               message.append('Evaluacion creada con exito!')
          #modificacion de evaluacion
          if all(v in request.POST for v in ["mod_nombre", "mod_fecha_inicio", "mod_fecha_fin", "evaluacion_id"]):
               print(request.POST)
               id = request.POST.get("evaluacion_id")
               obj = get_object_or_404(Evaluacion, id=id)
               nombre_evaluacion = request.POST.get("mod_nombre")
               fecha_inicio = request.POST.get("mod_fecha_inicio")
               fecha_fin = request.POST.get("mod_fecha_fin")
               fecha_incio = request.POST.get("mod_fecha_inicio")
               Evaluacion.objects.filter(id=id).update(nombre=nombre_evaluacion, fecha_Fin=fecha_fin, fecha_Inicio=fecha_incio)
               if "rubrica" in request.POST:
                    id_rubrica = request.POST.get("rubrica")
                    rubrica = get_object_or_404(Rubrica, id=id_rubrica)
                    evaluacion_rubrica = get_object_or_404(Evaluacion_Rubrica, id_Evaluación=obj)
                    rubrica = Rubrica.objects.get(id=rubrica)
                    Evaluacion_Rubrica.objects.filter(id_Evaluación=obj, id_Rúbrica=rubrica).update(id_Rúbrica=rubrica)
                    evaluacion_rubrica.refresh_from_db()
               obj.refresh_from_db()

     form = CreateFormEvaluacion()
     obj = Evaluacion.objects.all().order_by('-fecha_Inicio')
     context = {'object_list':obj, 'form':form, 'mensaje':message}
     return render(request,'Admin-landing/admin_evaluaciones_gestion2.html',context)



def evaluacion_view(request, evaluacion_id):
     evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
     rubrica_evaluacion = get_object_or_404(Evaluacion_Rubrica, id_Evaluación=evaluacion_id)
     curso_evaluacion = get_object_or_404(Evaluacion_Curso, id_Evaluación=evaluacion_id)
     rubrica = get_object_or_404(Rubrica, id=rubrica_evaluacion.id_Rúbrica.id)
     rubrica_path = rubrica.rúbrica.path
     curso = get_object_or_404(Curso, id=curso_evaluacion.id_Curso.id)
     context = dict()
     if request.method == 'POST':
          form_evaluadores = FormUsuarioEnEvaluacion(request.POST, id_evaluacion=evaluacion)
          if form_evaluadores.is_valid():
               usuarios_evaluacion = form_evaluadores.cleaned_data.get("evaluador")
               for id_usuario in usuarios_evaluacion:
                    usuario = get_object_or_404(User, id=id_usuario)
                    Usuario_Evaluacion.objects.create(id_Usuario=usuario, id_Evaluación=evaluacion)
     if request.GET.get('equipo'):
          equipo = request.GET.get('equipo')
          equipo_obj = Equipo.objects.get(id=equipo)
          miembros = Estudiante.objects.filter(id_Equipo = equipo_obj)
          context["miembros"] = miembros
          context["equipo"] = equipo_obj
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
     evaluados = Evaluacion_Equipo.objects.filter(id_Evaluación=evaluacion)
     evaluadores_aux=Usuario_Evaluacion.objects.filter(id_Evaluación=evaluacion)
     evaluadores = ((x.id_Usuario) for x in evaluadores_aux)
     lista_evaluados = ((x.id_Equipo.id) for x in evaluados)
     equipos = Equipo.objects.filter(id_Curso=curso).exclude(id__in=lista_evaluados)
     # evaluacion = get_object_or_404(Evaluacion, id=eval_id)
     
     context["curso"] = curso
     if curso.semestre == 1:
          context["semestre"] = "Otoño"
     elif curso.semestre == 2:
          context["semestre"] = "Primavera"
     else:
          context["semestre"] = "Verano"
     context["evaluadores"] = evaluadores
     context["evaluacion"] = evaluacion
     context["equipos"] = equipos
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
     form = FormUsuarioEnEvaluacion({}, id_evaluacion=id_evaluacion)
     data=dict()
     data['form'] = form.as_ul()
     return JsonResponse(data)

def delete_evaluadores(request):
     evaluador = request.GET.get('evaluador')
     evaluacion = request.GET.get('evaluacion')
     evaluacion_id = Evaluacion.objects.get(id=evaluacion)
     evaluador_id = User.objects.get(email=evaluador)
     instancia = Usuario_Evaluacion.objects.filter(id_Usuario=evaluador_id, id_Evaluación=evaluacion_id)[0]
     instancia.delete()
     return {}

def get_all_rubricas(request):
     form = FormSelectRubrica()
     data = dict()
     data["form"] = form.as_ul()
     return JsonResponse(data)
     


    






