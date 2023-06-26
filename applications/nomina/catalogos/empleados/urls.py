from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import ListaEmpleados, RegistrarEmpleados, ConsultaEmpleados

app_name = 'empleados'

urlpatterns = [
    path('lista/', ListaEmpleados.as_view(), name='lista'),
    path('registrar/', RegistrarEmpleados.as_view(), name='registrar'),
    path('consulta/<int:pk>', ConsultaEmpleados.as_view(), name='consulta'),
]