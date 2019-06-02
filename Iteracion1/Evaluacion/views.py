import csv
import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from Evaluacion.models import Evaluacion
from Relaciones.models import (Evaluacion_Curso, 
                              Evaluacion_Rubrica, 
                              Usuario_Evaluacion,
                              Evaluacion_Estudiante, 
                              Evaluacion_Equipo)
from Curso.models import Curso 
from Estudiante.models import Estudiante
from Nombre_Curso.models import Nombre_Curso
from Rubrica.models import Rubrica
from Equipo.models import Equipo
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404, HttpResponse
from .forms import (CreateFormEvaluacion, 
                         FormSelectRubrica, 
                         CreateEvaluacion, 
                         CreateRubricaEvaluacion, 
                         CreateCursoEvaluacion,
                         UpdateRubricaEvaluacion)
from Relaciones.forms import FormUsuarioEnEvaluacion



"""
Vistas para las paginas de evaluaciones.

@author Nicolás Machuca
"""


"""
Vista para la landing page de evaluadores

@author Nicolás Machuca
"""
class EvaluacionListView(ListView):
    template_name = 'Evaluadores-landing/evaluadores-landing.html'
    eval_details = Evaluacion.objects.all().order_by('-fecha_Inicio')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


"""
evaluacion_list_and_create: Vista de las evaluaciones para admin, permite 
crear y modificar evaluaciones.
@author Nicolás Machuca
"""
def evaluacion_list_and_create(request):
     message = []
     errors_message = []
     if request.method == 'POST':
          form = CreateFormEvaluacion(request.POST)
          # creacion de evaluacion
          form = CreateEvaluacion(request.POST)
          if form.is_valid():
               new_evaluacion = form.save()
               new_post = request.POST.copy()
               new_post['id_Evaluación'] = new_evaluacion.id
               form_rubrica = CreateRubricaEvaluacion(new_post).save()
               form_curso = CreateCursoEvaluacion(new_post).save()
               message.append('Evaluacion creada con exito!')
               
     form = CreateEvaluacion()
     form_rubrica = CreateRubricaEvaluacion()
     form_curso = CreateCursoEvaluacion()
     obj = Evaluacion.objects.all().order_by('-fecha_Inicio')
     print(request.POST)
     context = {'object_list':obj, 'form':form, 'mensaje':message, 
               'form_rubrica': form_rubrica , 'form_curso': form_curso, "errors": errors_message}
     return render(request, 'Admin-landing/admin_evaluaciones_gestion2.html',context)

"""
evaluacion_edit: edita la evaluacion indicada de acuerdo al formulario recibido por el metodo POST, luego
redirige a la pagina de listado de evaluaciones.

@author Nicolás Machuca
"""
def evaluacion_edit(request):
     message = []
     errors_message = []
     if request.method == 'POST':
          if "evaluacion_id" in request.POST:
               eval_id = request.POST.get('evaluacion_id')
               obj = get_object_or_404(Evaluacion, id=eval_id)
               edit_evaluacion = CreateEvaluacion(request.POST,instance=obj)
               if edit_evaluacion.is_valid():
                    rubrica_eval_obj = get_object_or_404(Evaluacion_Rubrica, id_Evaluación=obj)
                    edit_rubrica = UpdateRubricaEvaluacion(request.POST, instance=rubrica_eval_obj)
                    if edit_rubrica.is_valid():
                         eval_rubrica = edit_rubrica.save()
                    else:
                         errors_message.append("Error al modificar la rúbrica asociada")
                    evaluacion = edit_evaluacion.save()
               else:
                    errors_message.append("Error al modificar la evaluación")
     form = CreateEvaluacion()
     form_rubrica = CreateRubricaEvaluacion()
     form_curso = CreateCursoEvaluacion()
     obj = Evaluacion.objects.all().order_by('-fecha_Inicio')
     context = {'object_list':obj, 'form':form, 'mensaje':message, 
               'form_rubrica': form_rubrica , 'form_curso': form_curso, "errors": errors_message}
     return redirect('resumen-evaluaciones', permanent=True)

"""
evaluacion_view: Muestra la informacion (rubrica, evaluadores, equipos, presentadores) 
de la evaluacion asociada al id que se entrega como parametro, permite elegir equipo
presentadores y evaluadores
@author Nicolás Machuca

"""
def evaluacion_view(request, evaluacion_id):
     evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id)
     rubrica_evaluacion = get_object_or_404(Evaluacion_Rubrica, id_Evaluación=evaluacion)
     curso_evaluacion = get_object_or_404(Evaluacion_Curso, id_Evaluación=evaluacion)
     rubrica = get_object_or_404(Rubrica, id=rubrica_evaluacion.id_Rúbrica.id)
     rubrica_path = rubrica.rúbrica.path
     curso = get_object_or_404(Curso, id=curso_evaluacion.id_Curso.id)
     nombre_curso = get_object_or_404(Nombre_Curso, id_Curso=curso)
     context = dict()

     if request.method == 'POST':
          # formulario para agregar evaluadores
          form_evaluadores = FormUsuarioEnEvaluacion(request.POST, id_evaluacion=evaluacion)
          if form_evaluadores.is_valid():
               usuarios_evaluacion = form_evaluadores.cleaned_data.get("evaluadores")
               for id_usuario in usuarios_evaluacion:
                    usuario = get_object_or_404(User, id=id_usuario)
                    Usuario_Evaluacion.objects.create(id_Usuario=usuario, id_Evaluación=evaluacion)

     # Equipo que presenta
     if request.GET.get('equipo'):
          equipo = request.GET.get('equipo')
          equipo_obj = Equipo.objects.get(id=equipo)
          evalaucion.equipo_presentando = equipo_obj
          evaluacion.save(["equipo_presentando"])
          if request.method == 'POST':
               # formulario para agregar presentadores
               form_presentadores = FormAgregarPresentador(request.POST, evaluacion=evaluacion, equipo=equipo_obj)
               if form_presentadores.is_valid():
                    presentadores = form_presentadores.cleaned_data.get("presentadores")
                    for id_estudiante in presentadores:
                         estudiante = get_object_or_404(Estudiante, id=id_estudiante)
                         Evaluacion_Estudiante.objects.create(id_Estudiante=estudiante, id_Evaluación=evaluacion)
          miembros = Estudiante.objects.filter(id_Equipo = equipo_obj)
          miembros_no_presentando = []
          miembros_presentando = []
          for x in miembros:
               if not Evaluacion_Estudiante.objects.filter(id_Evaluación=evaluacion, id_Estudiante=x).exists():
                   miembros_no_presentando.append(x)
               else:
                    miembros_presentando.append(x)
          context["no_presentando"] = miembros_no_presentando 
          context["presentando"] = miembros_presentando
          context["miembros"] = miembros
          context["equipo"] = equipo_obj

     # Cargar rubrica asociada
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
     context["nombre_curso"] = nombre_curso.Nombre
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

"""
evaluacion_delete_view: Elimina la rubrica asociada al id que se entrega como parametro,
esta funcion se llama a partir del boton eliminar que aparece en la pagina para mostrar evaluaciones
al retornar se redirecciona a esta misma pagina.
@author Nicolás Machuca
"""
def evaluacion_delete_view(request, evaluacion_id):
     if request.method == "POST":
          obj = Evaluacion.objects.get(id=evaluacion_id)
          obj.delete()
     return redirect("resumen-evaluaciones", permanent=True)
       
"""
getting_details_evaluaciones_view: retorna un JSONresponse con los datos mas importantes asociados
a la evaluacion para ser visualizados en la pagina para mostrar evaluaciones.
@author Nicolás Machuca
"""
def getting_details_evaluaciones_view(request):
     my_id = request.GET.get('query_id')
     obj = Evaluacion.objects.get(id=my_id)
     data=dict()
     data['Fecha de inicio: '] = obj.fecha_Inicio
     data['Fecha fin: '] = obj.fecha_Fin
     data['Estado: '] = obj.is_Open
     return JsonResponse(data)

"""
get_evaluadores: Retorna por JsonResponse un formulario de tipo select multiple
con los Usuarios(evaluadores) que no estan asociados a la evaluacion cuyo id se recibe por GET.
@author Nicolás Machuca
"""
def get_evaluadores(request):
     my_id = request.GET.get('query_id')
     id_evaluacion = Evaluacion.objects.get(id=my_id)
     form = FormUsuarioEnEvaluacion({}, id_evaluacion=id_evaluacion)
     data=dict()
     data['form'] = form.as_table()
     return JsonResponse(data)

"""
get_presentadores: Retorna por JsonResponse un formulario de tipo select multiple
con los estudiantes de un equipo que no estan asociados a la evaluacion cuyos ids se reciben por GET.
@author Nicolás Machuca
"""
def get_presentadores(request):
     id_evaluacion = request.GET.get('query_id')
     id_equipo = request.GET.get('equipo')
     evaluacion = Evaluacion.objects.get(id=id_evaluacion)
     equipo = Equipo.objects.get(id=id_equipo)
     form = FormAgregarPresentador({}, evaluacion=evaluacion, equipo=equipo)
     data=dict()
     data['form'] = form.as_table()
     return JsonResponse(data)


"""
delete_evaluadores: Desasocia a un evaluador de una evaluacion, los ids para identificar a
cada uno se reciben por metodo GET.
@author: Nicolás Machuca 
"""
def delete_evaluadores(request):
     evaluador = request.GET.get('query_id')
     evaluacion = request.GET.get('query2')
     evaluacion_id = Evaluacion.objects.get(id=evaluacion)
     evaluador_id = User.objects.get(email=evaluador)
     instancia = Usuario_Evaluacion.objects.filter(id_Usuario=evaluador_id, id_Evaluación=evaluacion_id)[0]
     instancia.delete()

"""
delete_evaluadores: Desasocia a un estuidante de ser presentador, los ids para identificar a
la evaluacion y al equipo se reciben por metodo GET.
@author: Nicolás Machuca 
"""
def delete_presentadores(request):
     presentador = request.GET.get('query_id')
     evaluacion = request.GET.get('query2')
     evaluacion_id = Evaluacion.objects.get(id=evaluacion)
     presentador_id = Estudiante.objects.get(id=presentador)
     instancia = get_object_or_404(Evaluacion_Estudiante, id_Estudiante=presentador_id, id_Evaluación=evaluacion_id)
     instancia.delete()

"""
update_evaluacion: Envia por JsonResponse un formulario para modificar nombre,
fecha_Inicio, fecha_Fin y rubrica asociada de la evaluacion correspondiente al id
recibido por metodo GET.
@author: Nicolás Machuca
"""
def update_evaluacion(request):
     id_evaluacion = request.GET.get('query_id')
     obj = get_object_or_404(Evaluacion, id=id_evaluacion)
     obj_eval_rubrica = get_object_or_404(Evaluacion_Rubrica, id_Evaluación=obj)
     data = dict()
     form = CreateEvaluacion(instance=obj)
     form_rubrica = UpdateRubricaEvaluacion(instance=obj_eval_rubrica)
     data["form"] = form.as_ul()
     data["form_rubrica"] = form_rubrica.as_ul()
     return JsonResponse(data)

"""
get_all_rubricas: Retorna por JsonResponse un formulario de tipo select con todas las rubricas 
que estan creadas.

@deprecated
@author Nicolás Machuca
"""
def get_all_rubricas(request):
     form = CreateRubricaEvaluacion()
     data = dict()
     data["form"] = form.as_ul()
     return JsonResponse(data)


    






