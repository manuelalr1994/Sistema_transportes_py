from django.contrib import admin
from django.urls import path, include

app_name = 'utilerias'

urlpatterns = [
    path('cierre_semanas/', include('applications.fletes.utilerias.cierre_semanas.urls', namespace='cierre_semanas')),
]