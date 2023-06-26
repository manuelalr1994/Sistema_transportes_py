from django.contrib import admin
from django.urls import path, include

app_name = 'catalogos'

urlpatterns = [
    path('ubicaciones/', include('applications.nomina.catalogos.ubicaciones.urls', namespace='ubicaciones')),
    path('empresas/', include('applications.nomina.catalogos.empresas.urls', namespace='empresas')),
    path('semanas/', include('applications.nomina.catalogos.semanas.urls', namespace='semanas')),
    path('cuadrilleros/', include('applications.nomina.catalogos.cuadrilleros.urls', namespace='cuadrilleros')),
    path('labores/', include('applications.nomina.catalogos.labores.urls', namespace='labores')),
    path('campos/', include('applications.nomina.catalogos.campos_agricolas.urls', namespace='campos')),
    path('cultivos/', include('applications.nomina.catalogos.cultivos.urls', namespace='cultivos')),
    path('empleados/', include('applications.nomina.catalogos.empleados.urls', namespace='empleados')),
    path('puestos/', include('applications.nomina.catalogos.puestos.urls', namespace='puestos')),
]