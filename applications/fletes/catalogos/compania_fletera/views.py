from django.shortcuts import render
from django.urls import reverse_lazy
from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras
from django.views.generic import ListView, CreateView, DetailView
from applications.users.mixins import LoginAndActiveMixin, PermisoFletes
# from applications.nomina.catalogos.ubicaciones.models import ubicaciones
from . import forms

# Create your views here.

class RegistrarCompania(LoginAndActiveMixin, PermisoFletes, CreateView):
    model = CompaniasFleteras
    form_class = forms.FormularioCompania
    template_name = 'fletes/catalogos/compania_fletera/registro_compania_fletera.html'
    success_url = reverse_lazy('fletes:catalogos:compania_fletera:lista')
    login_url = reverse_lazy('users_app:user_login')

    # def form_valid(self, form):
    #     ubicacion = ubicaciones.objects.get(pk=self.request.COOKIES.get('ubicacion_usuario'))
    #     form.instance.ubicacion = ubicacion
    #     return super().form_valid(form)


class ListaCompanias(LoginAndActiveMixin, PermisoFletes, ListView):
    model = CompaniasFleteras
    template_name = 'fletes/catalogos/compania_fletera/lista_compania_fletera.html'
    login_url = reverse_lazy('users_app:user_login')
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}
        # ubicacion = ubicaciones.objects.get(pk=self.request.COOKIES.get('ubicacion_usuario'))
        compania_buscada = self.request.GET.get('compania_buscada')
        if compania_buscada is not None:
            context['lista_companias_fleteras'] = self.model.objects.filter(nombre__icontains=compania_buscada)
        else:
            context['lista_companias_fleteras'] = self.model.objects.all()
        
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ConsultarCompania(LoginAndActiveMixin, PermisoFletes, DetailView):
    model = CompaniasFleteras
    template_name = 'fletes/catalogos/compania_fletera/consulta_compania_fletera.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(ConsultarCompania, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context