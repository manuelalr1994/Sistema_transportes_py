from django.shortcuts import render

# Create your views here.
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros
from applications.nomina.catalogos.empresas.models import NomEmpresas
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from applications.users.mixins import LoginAndActiveMixin, PermisoNomina


# Modulo para crear cuadrilleros
class RegistrarCuadrilleros(LoginAndActiveMixin, PermisoNomina, CreateView):
    model = NomCuadrilleros
    form_class = forms.FormularioCuadrilleros
    template_name = 'nomina/catalogos/cuadrilleros/registro_cuadrilleros.html'
    success_url = reverse_lazy('nomina:catalogos:cuadrilleros:lista')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        # Generamos el nuevo codigo correspondiente a este cuadrillero
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        form.instance.codigo = codigo
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(RegistrarCuadrilleros, self).get_context_data(**kwargs)
        # Generamos el nuevo codigo correspondiente a este cuadrillero
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        context['codigo_actual'] = codigo
        return context


# Modulo para mostrar lista de cuadrilleros
class ListaCuadrilleros(LoginAndActiveMixin, PermisoNomina, ListView):
    model = NomCuadrilleros
    template_name = 'nomina/catalogos/cuadrilleros/cuadrilleros.html'
    login_url = reverse_lazy('users_app:user_login')
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}
        cuadrillero_buscado = self.request.GET.get('cuadrillero_buscado')
        if cuadrillero_buscado is not None:
            context['lista_cuadrilleros'] = NomCuadrilleros.objects.filter(activo=True, nombre__icontains=cuadrillero_buscado)
        else:
            context['lista_cuadrilleros'] = NomCuadrilleros.objects.filter(activo=True)
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# Consulta individual de Cuadrilleros
class ConsultarCuadrilleros(LoginAndActiveMixin, PermisoNomina, DetailView):
    model = NomCuadrilleros
    template_name = 'nomina/catalogos/cuadrilleros/consulta_cuadrilleros.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(ConsultarCuadrilleros, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


# Modulo para Actualizar Cuadrilleros
class ActualizarCuadrilleros(LoginAndActiveMixin, PermisoNomina, UpdateView):
    model = NomCuadrilleros
    form_class = forms.FormularioCuadrilleros
    template_name = 'nomina/catalogos/cuadrilleros/actualizar_cuadrilleros.html'
    success_url = reverse_lazy('nomina:catalogos:cuadrilleros:lista')
    login_url = reverse_lazy('users_app:user_login')


# Modulo para Inactivar Cuadrilleros
class EliminarCuadrilleros(LoginAndActiveMixin, PermisoNomina, DeleteView):
    model = NomCuadrilleros
    template_name = 'nomina/catalogos/cuadrilleros/nomcuadrilleros_confirm_delete.html'
    login_url = reverse_lazy('users_app:user_login')

    def post(self, request, *args, **kwargs):
        object = self.model.objects.get(codigo = kwargs['pk'])
        object.activo = False
        object.save()
        return redirect('nomina:catalogos:cuadrilleros:lista')

# Modulo que va enviar nombre de la empresa a la peticion AJAX
def CargarNombreEmpresa(request):
    id_empresa = request.GET.get('id_empresa')
    empresa = NomEmpresas.objects.get(id = id_empresa)
    data = {}
    data['nombre_empresa'] = empresa.nombre
    return JsonResponse(data)
