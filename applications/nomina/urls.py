from django.contrib import admin
from django.urls import path, include
from .home_nomina.views import HomeNomina
from django.contrib.auth.decorators import login_required

app_name = 'nomina'

urlpatterns = [
    path('catalogos/', include('applications.nomina.catalogos.urls', namespace='catalogos')),
    path('consultas/', include('applications.nomina.consultas.urls', namespace='consultas')),
    path('', login_required(HomeNomina), name='home')
]