from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'procesar_maquila'

urlpatterns = [
    # path('registrar/', RegistrarCampos.as_view(), name='registrar'),
    path('lista/', ListadoProcesarMaquila.as_view(), name='lista'),
    path('registrar/', ProcesarMaquila.as_view(), name='registrar'),
    path('cargar-lista-maquilas/', login_required(cargarListaMaquilas), name='cargarListaMaquilas'),
    path('cargar-maquila-modal/', login_required(cargarMaquilaModal), name='cargarMaquilaModal'),
    path('reporte-listado-maquila/', ProcesarMaquila.as_view(), name='reporteListadoMaquila'), # pendiente
]