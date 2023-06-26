from django.contrib import admin
from django.urls import path
from .views import RegistrarCampos, ListaCampos

app_name = 'campos'

urlpatterns = [
    path('registrar/', RegistrarCampos.as_view(), name='registrar'),
    path('lista/', ListaCampos.as_view(), name='lista'),
]