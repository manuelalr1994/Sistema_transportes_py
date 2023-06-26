from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'listados_nomina'

urlpatterns = [
    path('lista/', login_required(listadosNomina), name='lista'),
    path('cargar-lista-nomina/', cargarListaNomina, name='cargarListaNomina'),

    # REPORTES
    path('reporte-listado-camiones/', ReporteListadoCamiones.as_view(), name='reporteListadoCamiones'),
    path('reporte-listado-excel/', ReporteExcel.as_view(), name='reporteListadoExcel'),

]