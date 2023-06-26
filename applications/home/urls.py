from django.urls import path
from .views import *

app_name = 'home'

# Establecemos las URL de esta view
urlpatterns = [
    path('', UbicacionesHome.as_view(), name='home_ubicaciones'),
    path('modulos/', ModulosHome.as_view(), name='home_modulos'),
]