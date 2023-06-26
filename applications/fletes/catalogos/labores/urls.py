from django.contrib import admin
from django.urls import path
from .views import ListaLabores, RegistrarLabores

app_name = 'labores'

urlpatterns = [
    path('registrar/', RegistrarLabores.as_view(), name='registrar'),
    path('lista/', ListaLabores.as_view(), name='lista'),
]