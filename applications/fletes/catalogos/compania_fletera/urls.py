from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'compania_fletera'

# Establecemos las URL de esta view
urlpatterns = [
    path('registrar/', RegistrarCompania.as_view(), name='registrar'),
    path('lista/', ListaCompanias.as_view(), name='lista'),
    path('consultar/<int:pk>', ConsultarCompania.as_view(), name='consultar'),
]