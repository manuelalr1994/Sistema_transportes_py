from django.contrib import admin
from django.urls import path
from .views import ListaEmpresas

app_name = 'ubicaciones'

urlpatterns = [
    path('lista/', ListaEmpresas.as_view(), name='lista'),
]   