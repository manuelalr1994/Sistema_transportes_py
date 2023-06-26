from django.contrib import admin
from django.urls import path, include

app_name = 'consultas'

urlpatterns = [
        path('captura-jornales/', include('applications.nomina.consultas.captura_jornales.urls', namespace='captura_jornales')),
        path('modificacion-jornales/', include('applications.nomina.consultas.modificacion_jornales.urls', namespace='modificacion_jornales')),
]