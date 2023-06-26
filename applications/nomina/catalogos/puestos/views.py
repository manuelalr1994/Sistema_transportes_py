from multiprocessing import context
from django.shortcuts import render, redirect
from urllib import request
from django.urls import reverse_lazy
from .models import NomPuestos
from .forms import FormularioPuestos
from django.views.generic import ListView, CreateView, DetailView
from applications.users.mixins import LoginAndActiveMixin, PermisoNomina

# Create your views here.

# Modulo para mostrar lista de puestos (Elimina y Muestra)
class ListaPuestos(LoginAndActiveMixin, PermisoNomina, ListView):
    model = NomPuestos
    template_name = 'nomina/catalogos/puestos/lista_puestos.html'
    login_url = reverse_lazy('users_app:user_login')
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}

        puesto_buscada = self.request.GET.get('puesto_buscada')
        if puesto_buscada is not None:
            context['lista_puestos'] = NomPuestos.objects.filter(nombre__icontains=puesto_buscada)
            print(context['lista_puestos'])
        else:
            context['lista_puestos'] = NomPuestos.objects.filter()
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class RegistrarPuestos(LoginAndActiveMixin, PermisoNomina, CreateView):
    model = NomPuestos
    form_class = FormularioPuestos
    template_name = "nomina/catalogos/puestos/registro_puestos.html"
    success_url = reverse_lazy('nomina:catalogos:puestos:lista')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):

        # Generamos el nuevo codigo correspondiente a esta labor
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        form.instance.codigo = codigo
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegistrarPuestos, self).get_context_data(**kwargs)

        # Generamos el nuevo codigo correspondiente a esta labor
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        context['codigo_actual'] = codigo
        return context

# Consulta individual de Puestos
class ConsultarPuestos(LoginAndActiveMixin, PermisoNomina, DetailView):
    model = NomPuestos
    template_name = "nomina/catalogos/puestos/consulta_puestos.html"
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(ConsultarPuestos, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


# class ConsultarPuestos(TemplateView):
#    template_name = 'nomina/catalogos/puestos/consulta_puestos.html'