from django.urls import path
from .views import *

app_name = 'fletes'

# Establecemos las URL de esta view
urlpatterns = [
    path('lista-estado-cuenta/', ListaEstadoCuenta.as_view(), name='ListaEstadoCuenta'),
    path('estado-cuenta/', EstadoCuenta.as_view(), name='EstadoCuenta'),
    path('reporte_estado_cuenta/', reporteEstadoCuenta.as_view(), name='reporteEstadoCuenta'),
]