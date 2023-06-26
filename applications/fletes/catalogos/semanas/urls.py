from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import RegistrarSemanas, ListaTiposSemanas, ConsultarTiposSemanas

app_name = 'semanas'

urlpatterns = [
    path('registrar/', login_required(RegistrarSemanas), name='registrar'),
    path('lista/', ListaTiposSemanas.as_view(), name='lista'),
    path('consultar/<int:pk>', ConsultarTiposSemanas.as_view(), name='consultar'),
]   