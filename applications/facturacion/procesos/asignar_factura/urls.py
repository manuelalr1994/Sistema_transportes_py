from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'asignar_factura'

urlpatterns = [
    # path('registrar/', RegistrarCampos.as_view(), name='registrar'),
    path('asignar-factura/', AsignarFactura.as_view(), name='asignarFactura'),
    path('estado-cuenta-facturas/', EstadoCuentaFacturas.as_view(), name='estadoCuentaFacturas'),
    path('cargar-lista-facturas/', login_required(cargarListaRemisiones), name='cargarListaFacturas'),
    path('cargar-remision/', login_required(cargarRemision), name='cargarRemision'),
    path('cargar-desglose/', login_required(cargarDesglose), name='cargarDesglose'),
]
    