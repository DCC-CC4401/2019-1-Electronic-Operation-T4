import csv
import os
try: 
    import unicodecsv as ucsv
except ImportError:
    os.system('pip install unicodecsv')
import re
import subprocess
try:
    import xlrd as xls
except ImportError:
    os.system('pip install xlrd')
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.core.files import File
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
    path = settings.MEDIA_ROOT.join(file_form.name)
    with open(f'{file_form.name}', 'wb+') as destination:
        for chunk in file_form.chunks():
            destination.write(chunk)
def xls_to_csv(file_form,nombre,archivo):
    upload_file(archivo)
    nombre = file_form.name
    nombre_csv = file_form.name.split('.xls')[0]+'.csv'
    path_xls=file_form.name
    path_csv=nombre_csv
    wb = xls.open_workbook(path_xls)
    sheet_name = wb.sheet_names()
    sh = wb.sheet_by_index(0) 
    with open(path_csv,'w') as your_csv_file:
        wr = ucsv.writer(your_csv_file,encoding="utf-8", quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        os.remove(path_xls)
        file_csv = File(your_csv_file)
        Rubrica.objects.create(nombre=nombre, rúbrica=file_csv)
        file_csv.close()

"""
rubrica_list_and_create: Vista para el resumen de las rubricas, permite crear, eliminar y ver
como lista las rubricas creadas.
@author Joaquin Cruz
"""


def rubrica_list_and_create(request):
     message = list()
     message_malo = list()
     if request.method == 'POST':
          form = CreateForm(request.POST, request.FILES)
          if form.is_valid():
               nombre = form.cleaned_data.get("nombre")
               archivo = form.cleaned_data.get("rubrica")
               name_regex = re.compile("^\w+\w*$")
               file_regex = re.compile("^\w+\.(xls|csv)$")
               archivo_name = archivo.name
               if name_regex.match(nombre) and file_regex.match(archivo_name):
                    if re.compile("^\w+\.xls$").match(archivo_name):
                        xls_to_csv(archivo,nombre,archivo)
                    else:
                        upload_file(archivo)
                        Rubrica.objects.create(nombre=nombre, rúbrica=archivo)
                    message.append('Rubrica creada con exito!')
               if not name_regex.match(nombre):
                    message.append(f'Error de formato en el Nombre de la rubrica {nombre}')
               if not file_regex.match(archivo_name):
                    message.append(f'Error en el formato del archivo, debe ser xls o csv')
     form = CreateForm()
     obj = Rubrica.objects.all()
     context = {'object_list': obj, 'form': form, 'mensaje': message}
     return render(request, 'Admin-landing/admin_rubricas_gestion.html', context)


"""
rubrica_delete_view: funcion que genera la eliminacion de las rubricas 
a partir del boton que aparece en la lista, se redirecciona a la misma pagina
de la cual se estaba con el hecho de que no aparece la rubrica eliminada
@author Joaquin Cruz
"""


def rubrica_delete_view(request, rubrica_id):
    if request.method == 'POST':
        # cambiar por ahora este path
        obj = Rubrica.objects.get(id=rubrica_id)
        file_path = obj.rúbrica.path
        if os.path.isfile(file_path):
            os.remove(file_path)
        obj.delete()
        return redirect("resumen-rubricas", permanent=True)



"""
rubrica_detail_view: genera la vista en detalle de cada rubrica,
para esto se tiene que abrir el archivo csv desplegando asi su informacion
@author Joaquin Cruz
"""


def rubrica_detail_view(request, rubrica_id):
    my_rubrica = get_object_or_404(Rubrica, id=rubrica_id)
    rubrica_path = my_rubrica.rúbrica.path
    context_data = dict()
    try:
        with open(rubrica_path, newline='') as my_file:
            reader = csv.reader(my_file, delimiter=',')
            data_rubrica = list()
            max_length = 0
            for row in reader:
                columna = list()
                for dato in row:
                    columna.append(dato)
                data_rubrica.append(columna)
                if max_length < len(columna):
                    max_length = len(columna)
            context_data['nombre'] = my_rubrica.nombre
            context_data['rubrica'] = data_rubrica
            context_data['max_length'] = max_length
            context_data['duracion_min'] = my_rubrica.duración_Mínima
            context_data['duracion_max'] = my_rubrica.duración_Máxima
            return render(request, 'Ficha-rubricas/detalles_rubrica.html', context_data)
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
    with open(obj.rúbrica.path, newline='') as my_file:
        reader = csv.reader(my_file, delimiter=',')
        count = 0
        for row in reader:
            if count != 0:
                data[f'Aspecto{count}'] = row[0]
            count += 1
    return JsonResponse(data)


# TODO: Validacion  y el update de las rubricas :D
