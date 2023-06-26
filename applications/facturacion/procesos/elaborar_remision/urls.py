from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'elaborar_remision'

urlpatterns = [
    # path('registrar/', RegistrarCampos.as_view(), name='registrar'),
    path('lista/', ListadoRemision.as_view(), name='lista'),
    path('estado-cuenta-remision/', EstadoCuentaRemision.as_view(), name='estadoCuentaRemision'),
    path('cargar-lista-remisiones/', login_required(cargarListaRemisiones), name='cargarListaRemisiones'),
    path('cargar-campo-agricola/', login_required(cargarCampoAgricola), name='cargarCampoAgricola'),
    path('cargar-semanas-remision/', login_required(cargarSemanasRemision), name='cargarSemanasRemision'),
    path('cargar-desglose/', login_required(cargarDesglose), name='cargarDesglose'),

]