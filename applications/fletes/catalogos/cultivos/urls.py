from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import RegistrarCultivo, ListaCultivos, cargarCultivos, cargarVariedades

app_name = 'cultivos'

urlpatterns = [
    path('registrar/', login_required(RegistrarCultivo), name = 'registrar'),
    path('lista/', ListaCultivos.as_view(), name = 'lista'),
    path('cargarCultivos/', cargarCultivos, name = 'cargarCultivos'),
    path('cargarVariedades/', cargarVariedades, name = 'cargarVariedades'),
]