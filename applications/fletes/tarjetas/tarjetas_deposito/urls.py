from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.urls import path
from .views import *

app_name = 'tarjetas_deposito'

urlpatterns = [
    path('lista/', permission_required(listaTarjetas), name='lista'),
]