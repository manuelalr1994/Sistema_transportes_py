from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .home_facturacion.views import HomeFacturacion

app_name ='facturacion'

urlpatterns = [
    path('consultas/', include('applications.facturacion.consultas.urls', namespace='consultas')),
    path('procesos/', include('applications.facturacion.procesos.urls', namespace='procesos')),
    path('reportes/', include('applications.facturacion.reportes.urls', namespace='reportes')),
    path('utilerias/', include('applications.facturacion.utilerias.urls', namespace='utilerias')),
    path('', login_required(HomeFacturacion), name="home"),
]