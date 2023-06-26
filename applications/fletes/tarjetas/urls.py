from django.contrib import admin
from django.urls import path, include

app_name = 'tarjetas'

urlpatterns = [
    path('tarjetas_deposito/', include('applications.fletes.tarjetas.tarjetas_deposito.urls', namespace='tarjetas_deposito')),
]