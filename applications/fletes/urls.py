from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .home_fletes.views import HomeFletes

app_name ='fletes'

urlpatterns = [
    path('catalogos/', include('applications.fletes.catalogos.urls', namespace='catalogos')),
    path('procesos/', include('applications.fletes.procesos.urls', namespace='procesos')),
    path('tarjetas/', include('applications.fletes.tarjetas.urls', namespace='tarjetas')),
    path('utilerias/', include('applications.fletes.utilerias.urls', namespace='utilerias')),
    path('', login_required(HomeFletes), name="home"),
]