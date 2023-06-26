from django.contrib import admin
from django.urls import path, include

app_name ='consultas'

urlpatterns = [
    path('fletes/', include('applications.facturacion.consultas.fletes.urls', namespace='fletes')),
]