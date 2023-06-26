from django.contrib import admin
from django.urls import path
from .views import ModificacionJornales

app_name = 'puestos'

urlpatterns = [
    path('registrar/', ModificacionJornales.as_view(), name='registrar'),
]