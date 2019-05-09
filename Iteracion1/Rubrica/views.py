import csv
import os
import re
import subprocess
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse,Http404
from django.views.generic import ListView, DetailView, View
# Create your views here.
from .models import Rubrica
from .forms import CreateForm
"""
Vistas para las pagina de rubricas de los admin, no he visto nada de los
evaluadores.
@author Joaquin Cruz
"""
def upload_file(file_form):
     try:
          import xlrd as xls
     except ImportError:
          os.system('pip install xlrd')
     finally:
          with open(f'{file_form.name}','wb+') as destination:
               for chunk in file_form.chunks():
                    destination.write(chunk)
          if 'xls' in file_form.name.split('.'):
               wb = xls.open_workbook(f'{file_form.name}')
               sh = wb.sheet_by_name('Hoja 1')
               with open(file_form.name[:-3]+'.csv','wb'):
                    wr = csv.writer()
def verificar_extension(file_name):
     pass
     # TODO 
     
"""
rubrica_list_and_create: Vista para el resumen de las rubricas, permite crear, eliminar y ver
como lista las rubricas creadas.
@author Joaquin Cruz
"""
def rubrica_list_and_create(request):
     message = list()
     message_malo = list()
     if request.method == 'POST':
          form = CreateForm(request.POST,request.FILES)
          if form.is_valid():
               nombre = form.cleaned_data.get("nombre")
               archivo = form.cleaned_data.get("rubrica")

               archivo_name= archivo.name
               Rubrica.objects.create(nombre=nombre,rúbrica=archivo)
               message.append('Rubrica creada con exito!')
     form = CreateForm()
     obj = Rubrica.objects.all()
     context = {'object_list':obj,'form':form,'mensaje':message}
     return render(request,'Admin-landing/admin_rubricas_gestion.html',context)
"""
rubrica_delete_view: funcion que genera la eliminacion de las rubricas 
a partir del boton que aparece en la lista, se redirecciona a la misma pagina
de la cual se estaba con el hecho de que no aparece la rubrica eliminada
@author Joaquin Cruz
"""
def rubrica_delete_view(request,rubrica_id):
     if request.method=='POST':
          #cambiar por ahora este path
          obj = Rubrica.objects.get(id=rubrica_id)
          file_path = obj.rúbrica.path
          if os.path.isfile(file_path):
               os.remove(file_path)
          obj.delete()
          return redirect("resumen-rubricas",permanent=True)
def rubrica_delete_view(request):
     if request.method == "POST":
          name = request.POST['nombre_rubrica']
          file = request.FILES['archivo-rubrica']
          name_regex = re.compile("^\w+$")
          file_regex = re.compile("^\w+\.(exl|csv)$")
"""
rubrica_detail_view: genera la vista en detalle de cada rubrica,
para esto se tiene que abrir el archivo csv desplegando asi su informacion
@author Joaquin Cruz
"""
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
     
"""
getting_aspects_view: funcion que genera los aspectos de 
las rubricas a partir de su id. Esta se llama asincronamente 
desde el html.
@author Joaquin Cruz
"""
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


          
#TODO: Generar la creacion y el update de las rubricas :D