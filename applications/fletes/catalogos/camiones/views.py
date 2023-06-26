from django.shortcuts import render
from django.urls import reverse_lazy
from applications.fletes.catalogos.camiones.models import Camiones
from django.views.generic import ListView, CreateView, DetailView
from applications.users.mixins import LoginAndActiveMixin, PermisoFletes
from . import forms

# Create your views here.

class RegistrarCamion(LoginAndActiveMixin, PermisoFletes, CreateView):
    model = Camiones
    form_class = forms.FormularioCamiones
    template_name = 'fletes/catalogos/camiones/registro_camiones.html'
    success_url = reverse_lazy('fletes:catalogos:camiones:lista')
    login_url = reverse_lazy('users_app:user_login')

class ListaCamiones(LoginAndActiveMixin, PermisoFletes, ListView):
    model = Camiones
    template_name = 'fletes/catalogos/camiones/lista_camiones.html'
    login_url = reverse_lazy('users_app:user_login')
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}
        camion_buscado = self.request.GET.get('camion_buscado')
        if camion_buscado is not None:
            context['lista_camiones'] = self.model.objects.filter(nombre__icontains=camion_buscado)
        else:
            context['lista_camiones'] = self.model.objects.all()

        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ConsultarCamion(LoginAndActiveMixin, PermisoFletes, DetailView):
    model = Camiones
    template_name = 'fletes/catalogos/camiones/consulta_camiones.html'
    login_url = reverse_lazy('users_app:user_login')