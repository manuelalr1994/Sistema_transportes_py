from django.contrib import admin
from django.urls import path
from .views import ListaPuestos, RegistrarPuestos, ConsultarPuestos

app_name = 'puestos'

urlpatterns = [
    path('lista/', ListaPuestos.as_view(), name='lista'),
    path('registrar/', RegistrarPuestos.as_view(), name='registrar'),
    path('consulta/<pk>/', ConsultarPuestos.as_view(), name='consulta'),
]