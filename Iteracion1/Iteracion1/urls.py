"""Iteracion1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import *
from Rubrica.views import ( getting_aspects_view,
                            rubrica_detail_view,
                            rubrica_delete_view,
                            rubrica_list_and_create,
                            rubrica_edit_view,
                            update_rubrica_view,
                            landing_evaluadores_rubricas_view)

from Evaluacion.views import (EvaluacionListView, 
                                evaluacion_view,
                                getting_details_evaluaciones_view,
                                evaluacion_list_and_create,
                                evaluacion_delete_view,
                                get_evaluadores,
                                delete_evaluadores,
                                get_all_rubricas,
                                get_presentadores,
                                update_evaluacion, 
                                evaluacion_edit,
                                delete_presentadores, 
                                evaluando,
                                evaluando_evaluador,
                                validar_envio_evaluacion,
                                evaluando_terminar,
                                evaluando_terminar_evaluador)

from Usuario.views import (usuario_delete_view, 
                            usuario_modificar_view)

from django.contrib.auth import logout

urlpatterns = [
    path('prueba/', evaluacion_prueba), # vista de prueba para el formulario de creacción de evaluación
    path('admin/', admin.site.urls),
    path('landing1/', landing_evaluaciones_view),
    path('registro/', registro, name='registro'),
    path('login/',login, name='login'),
    path('logout/',logout_view,name='logout'),

    path('evaluadores/',landing_evaluadores_view),
    path('evaluadores/modificar/<username>', usuario_modificar_view),
    path('evaluadores/eliminar/<username>', usuario_delete_view),
    
    path('',home_view),
    path('evaluaciones/',landing_evaluaciones_view, name="resumen-evaluaciones"),#modificado
    path('ficha-evaluacion/', ficha_evaluacion_admin_view),
    path('rubricas/',landing_rubricas_view,name="resumen-rubricas"), #modificado
    path('ajax/datos',getting_aspects_view,name="getting_aspects"),
    path('rubricas/eliminar/<uuid:rubrica_id>',rubrica_delete_view),
    path('rubricas/detalles/<uuid:rubrica_id>',rubrica_detail_view,name="ver_rubrica"),
    path('landing/evaluadores', EvaluacionListView.as_view(), name='evaluadores-landing'),
    path('evaluacion/<uuid:evaluacion_id>', evaluacion_view, name='evaluacion'),
    path('ajax/evaluacion', getting_details_evaluaciones_view, name="detalles_evaluacion"),
    path('evaluaciones/eliminar/<uuid:evaluacion_id>', evaluacion_delete_view, name='eliminar_rubrica'),
    path('rubricas/editar/<uuid:rubrica_id>',rubrica_edit_view,name="edicion_rubrica"),
    path('evaluaciones/editar', evaluacion_edit, name="editar_evaluacion"),
    path('evaluacion/<uuid:evaluacion_id>/<uuid:equipo_id>', evaluacion_delete_view ),
    path('evaluacion/evaluar/<uuid:evaluacion_id>', evaluando, name="evaluando"),
    path('evaluacion/evaluar/terminado/<uuid:id_evaluacion>', evaluando_terminar, name="evaluando_terminado"),
    path('evaluacion/evaluador/evaluar/<uuid:evaluacion_id>', evaluando_evaluador, name="evaluador_evaluando"),
    path('evaluacion/evaluador/terminado/<uuid:id_evaluacion>', evaluando_terminar_evaluador,name="evaluando_terminado_evaluador"),


    path('ajax/evaluacion/evaluadores', get_evaluadores, name="lista_evaluadores"),
    path('ajax/evaluacion/evaluador/eliminar', delete_evaluadores, name="delete_evaluador"),
    path('ajax/evaluacion/evaluando/enviar', validar_envio_evaluacion, name="validar_evaluacion"),
    path('ajax/update_rubrica',update_rubrica_view,name="update_rubrica"),
    path('ajax/evaluacion/presentador/eliminar', delete_presentadores, name="delete_presentador"),
    path('ajax/evaluacion/update', update_evaluacion, name="update_evaluacion"),
    path('ajax/evaluacion/presentadores', get_presentadores, name="lista_presentadores"),
    path('rubricas/evaluadores/landing', landing_evaluadores_rubricas_view, name="rubricas_evaluadores")
]