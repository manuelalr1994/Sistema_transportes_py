from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'cuadrilleros'

urlpatterns = [
    path('registrar/', RegistrarCuadrilleros.as_view(), name='registrar'),
    path('lista/', ListaCuadrilleros.as_view(), name='lista'),
    path('actualizar/<int:pk>', ActualizarCuadrilleros.as_view(), name='actualizar'),
    path('consultar/<int:pk>', ConsultarCuadrilleros.as_view(), name='consultar'),
    path('eliminar/<int:pk>', EliminarCuadrilleros.as_view(), name='eliminar'),
    #path('cargar_nombre_empresa/', CargarNombreEmpresa), <---- Ejemplo para AJAX menu dinamico
]