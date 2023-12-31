"""SistemaGSMO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluimos URLs de Home
    path('', include('applications.home.urls', namespace='home')),
    # Incluimos URLs de Usuarios
    re_path('accounts/', include('applications.users.urls')),
    # Incluimos URLs de Nomina
    path('nomina/', include('applications.nomina.urls', namespace='nomina')),
    # Incluimos URLs de Facturacion
    path('facturacion/', include('applications.facturacion.urls', namespace='facturacion')),
    # Incluimos URLs de Fletes
    path('fletes/', include('applications.fletes.urls', namespace='fletes')),
    # Incluimos URLs de Flotilla
    path('flotilla/', include('applications.flotilla.urls', namespace='flotilla')),
]
