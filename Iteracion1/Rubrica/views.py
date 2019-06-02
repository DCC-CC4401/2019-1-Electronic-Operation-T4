import csv
import os
try:
    import unicodecsv as ucsv
except ImportError:
    os.system('pip install unicodecsv')
import re
import subprocess
import json
try:
    import xlrd as xls
except ImportError:
    os.system('pip install xlrd')
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.core.files import File
from django.views.generic import ListView, DetailView, View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
# Create your views here.
from .models import Rubrica
from .forms import CreateForm
"""
Vistas para las pagina de rubricas de los admin.
@author Joaquin Cruz
"""

"""
Crea el archivo correspondiente a la rubrica al crear una nueva rubrica.
@author Joaquin Cruz
"""


def upload_file(file_form):
    path = settings.MEDIA_ROOT.join(file_form.name)
    with open(f'{file_form.name}', 'wb+') as destination:
        for chunk in file_form.chunks():
            destination.write(chunk)


"""
Convierte un archivo excel a uno csv ingresado por el formulario del usuario
@author Joaquin Cruz
"""


def xls_to_csv(file_form, name, archivo):
    upload_file(archivo)
    nombre = file_form.name
    nombre_csv = file_form.name.split('.xls')[0]+'.csv'
    path_xls = file_form.name
    path_csv = nombre_csv
    wb = xls.open_workbook(path_xls)
    sh = wb.sheet_by_index(0)
    with open(f"media/{path_csv}", 'r+') as your_csv_file:
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
        for rownum in range(sh.nrows):
            x = sh.row_values(rownum)
            wr.writerow(x)
        file_csv = File(your_csv_file)
        Rubrica.objects.create(nombre=name, rúbrica=file_csv)
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
                    xls_to_csv(archivo, nombre, archivo)
                else:
                    upload_file(archivo)
                    Rubrica.objects.create(nombre=nombre, rúbrica=archivo)
                message.append('Rubrica creada con exito!')
            if not name_regex.match(nombre):
                message.append(
                    f'Error de formato en el Nombre de la rubrica {nombre}')
            if not file_regex.match(archivo_name):
                message.append(
                    f'Error en el formato del archivo, debe ser xls o csv')
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


"""
Verifica que los datos ingresados por el usuario hayan sido correctos
@param data: dict: diccionario del json creado con los datos
@return True si los datos son validos
@author Joaquin Cruz
"""


def clean_update(data: dict):

    nombre_rubrica = data['nombre_tabla']
    info_rubrica = data['rubrica']
    if len(info_rubrica) <= 1 or nombre_rubrica == "":
        return False
    regex_temas = re.compile("[a-zA-Z0-0,\.!\? ]*")
    puntajes = info_rubrica[0]
    if puntajes[0] != "":
        return False
    for puntaje in puntajes[1:]:
        if not re.compile("^\d\.\d$").match(puntaje):
            return False
    for row in info_rubrica[1:]:
        for entry in row:
            if not regex_temas.match(entry):
                print(entry)
                return False
    return re.compile("^\w+$").match(nombre_rubrica)


"""
Controlador que hace el update a los datos asincronamente en
la base de datos, no pide cookie csrf
@param request: parametro de la peticion http hecha
@return Json con mensaje si todo esta en orde, tira error 404 si hay un error (todo: mejorar a mensaje de error)
@author Joaquin Cruz
"""
@csrf_exempt
def update_rubrica_view(request):
    if request.method == "POST":
        datos = json.loads(request.body)
        rubrica_id = datos['id']
        nombre = datos['nombre_tabla']
        rubrica = datos['rubrica']
        tiempo_min = datos['tiempo_min']
        tiempo_max = datos['tiempo_max']
        if clean_update(datos):
            obj = get_object_or_404(Rubrica, id=rubrica_id)
            rubrica_path = obj.rúbrica.path
            obj.nombre = nombre
            with open(rubrica_path, mode="w") as my_file:
                writer = csv.writer(my_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_ALL)
                for row in rubrica:
                    writer.writerow(row)
            obj.duración_Mínima = tiempo_min
            obj.duración_Máxima = tiempo_max
            obj.save()
            responseData = {"ok": "Todo salio ok!"}
            return JsonResponse(responseData)
        else:
            raise Http404('Datos mal ingresados')


"""
Controlador para la vista del update
@param request: cabecera de la peticion http
@param rubrica_id: id de la rubrica a hacer el update
@author Joaquin Cruz 
"""
@ensure_csrf_cookie
def rubrica_edit_view(request, rubrica_id):
    try:
        obj = Rubrica.objects.get(id=rubrica_id)
        data = dict()
        data["nombre_rubrica"] = obj.nombre
        rubrica_path = obj.rúbrica.path
        with open(rubrica_path, newline='') as my_file:
            reader = csv.reader(my_file, delimiter=',')
            data_rubrica = list()
            for row in reader:
                fila = list()
                for dato in row:
                    fila.append(dato)
                data_rubrica.append(fila)
            data["puntajes"] = data_rubrica[0]
            data_rubrica.pop(0)
            data["rubrica"] = data_rubrica
            data["id"] = obj.id
            data["duracion_min"] = obj.duración_Mínima
            data["duracion_max"] = obj.duración_Máxima
            return render(request, 'Ficha-rubricas/ficha_rubrica_admin.html', data)
    except FileNotFoundError:
        raise Http404("No se pudo encontrar la rubrica solicitada")


"""
funcion para el landing de los evaluadores de las rubricas
@author Joaquin Cruz
"""
# TODO: Que cargue solo las rubricas del evaluador.


def landing_evaluadores_rubricas_view(request):
    obj = Rubrica.objects.all()
    context = {'object_list': obj}
    return render(request, 'Ficha-rubricas/landing_evaluador_rubricas.html', context)

# TODO: Validacion de la suma de puntajes
# TODO: Refactor de leer la rubrica a una funcion
# TODO: Añadir los tiempos de la presentacion
