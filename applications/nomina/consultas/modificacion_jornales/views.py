from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ModificacionJornales(TemplateView):
    template_name = 'nomina/consultas/modificacion_jornales/modificacion_jornales.html'