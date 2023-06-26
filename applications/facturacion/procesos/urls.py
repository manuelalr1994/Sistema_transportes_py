from django.contrib import admin
from django.urls import path, include

app_name = 'procesos'

urlpatterns = [
    path('procesar-maquila/', include('applications.facturacion.procesos.procesar_maquila.urls', namespace='procesar_maquila')),
    path('elaborar-remision/', include('applications.facturacion.procesos.elaborar_remision.urls', namespace='elaborar_remision')),
    path('asignar-factura/', include('applications.facturacion.procesos.asignar_factura.urls', namespace='asignar_factura')),
]