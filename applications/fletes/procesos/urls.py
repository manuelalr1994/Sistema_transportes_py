from django.contrib import admin
from django.urls import path, include

app_name = 'procesos'

urlpatterns = [
    path('capturas_fleteras/', include('applications.fletes.procesos.capturas_fleteras.urls', namespace='capturas_fleteras')),
    path('listados_nomina/', include('applications.fletes.procesos.listados_nomina.urls', namespace='listados_nomina')),
]