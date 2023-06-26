from django.contrib import admin
from django.urls import path, include

app_name = 'catalogos'

urlpatterns = [
    path('ubicaciones/', include('applications.fletes.catalogos.ubicaciones.urls', namespace='ubicaciones')),
    path('empresas/', include('applications.fletes.catalogos.empresas.urls', namespace='empresas')),
    path('semanas/', include('applications.fletes.catalogos.semanas.urls', namespace='semanas')),
    path('cuadrilleros/', include('applications.fletes.catalogos.cuadrilleros.urls', namespace='cuadrilleros')),
    path('labores/', include('applications.fletes.catalogos.labores.urls', namespace='labores')),
    path('campos/', include('applications.fletes.catalogos.campos_agricolas.urls', namespace='campos')),
    path('cultivos/', include('applications.fletes.catalogos.cultivos.urls', namespace='cultivos')),
    path('compania_fletera/', include('applications.fletes.catalogos.compania_fletera.urls', namespace='compania_fletera')),
    path('camiones/', include('applications.fletes.catalogos.camiones.urls', namespace='camiones')),
]