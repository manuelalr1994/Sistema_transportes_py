from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'empresas'

# Establecemos las URL de esta view
urlpatterns = [
    path('registrar/', RegistrarEmpresas.as_view(), name='registrar'),
    path('lista/', ListaEmpresas.as_view(), name='lista'),
    path('actualizar/<int:pk>', ActualizarEmpresas.as_view(), name='actualizar'),
    path('consultar/<int:pk>', ConsultarEmpresas.as_view(), name='consultar'),
    path('eliminar/<int:pk>', EliminarEmpresas.as_view(), name='eliminar'),
]