from django.contrib import admin
from django.urls import path
from .views import ListaUbicaciones

app_name = 'ubicaciones'

urlpatterns = [
    path('lista/', ListaUbicaciones.as_view(), name='lista'),
]   