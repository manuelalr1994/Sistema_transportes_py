from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'camiones'

# Establecemos las URL de esta view
urlpatterns = [
    path('registrar/', RegistrarCamion.as_view(), name='registrar'),
    path('lista/', ListaCamiones.as_view(), name='lista'),
    path('consultar/<int:pk>', ConsultarCamion.as_view(), name='consultar'),
]