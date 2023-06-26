from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'cierre_semanas'

urlpatterns = [
    path('cierre/', login_required(cerrarSemana), name='cierre'),
]