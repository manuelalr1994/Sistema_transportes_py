from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'captura_jornales'

urlpatterns = [
    path('registrar/', login_required(RegistrarCaptura), name='registrar'),
    path('cargar_datos_empleado/', cargarDatosEmpleado, name='cargarDatosEmpleado'),
    path('cargar_dias_empleado/', cargarDiasEmpleado, name='cargarDiasEmpleado'),
    # path('modificar/', login_required(ModificarCaptura), name='modificar'),

    # # CARGA DE DATOS A AJAX
    # path('cargar_variedad/', cargarVariedad, name='cargarVariedad'),
    # path('cargar_cuadrillero/', cargarCuadrillero, name='cargarCuadrillero'),
    # path('cargar_semana/', cargarSemana, name='cargarSemana'),
    # path('cargar_fecha/', cargarFecha, name='cargarFecha'),
    # path('cargar_tipo_semana/', cargarTipoSemana, name='cargarTipoSemana'),
    # path('cargar_lista_capturas/', cargarListaCapturas, name='cargarListaCapturas'),
    # path('cargar_captura/', cargarCaptura, name='cargarCaptura'),
    # path('verificar_semana_cerrada/', verificarSemanaCerrada, name='verificarSemanaCerrada'),

    # # REPORTES
    # path('reporte_listado_camiones/', ReporteListadoCamiones.as_view(), name='reporteListadoCamiones'),
    # path('reporte_bitacora/', ReporteBitacora.as_view(), name='reporteBitacora'),

]