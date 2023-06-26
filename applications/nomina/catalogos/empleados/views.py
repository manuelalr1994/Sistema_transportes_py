from django.shortcuts import render
from django.urls import reverse_lazy
from .models import NomEmpleado
from .forms import FormularioEmpleados
from django.views.generic import TemplateView, CreateView, ListView

class RegistrarEmpleados(CreateView):
    model = NomEmpleado
    template_name = 'nomina/catalogos/empleados/registro_empleados.html'
    form_class = FormularioEmpleados
    success_url = reverse_lazy('nomina:catalogos:empleados:lista')


class ListaEmpleados(ListView):
    model = NomEmpleado
    template_name = 'nomina/catalogos/empleados/lista_empleados.html'
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}
        empleado_buscado = self.request.GET.get('empleado_buscado')
        if empleado_buscado is not None:
            context['lista_empleados'] = NomEmpleado.objects.filter(activo=True, nombre__icontains=empleado_buscado)
        else:
            context['lista_empleados'] = NomEmpleado.objects.filter(activo=True)
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ConsultaEmpleados(TemplateView):
    model = NomEmpleado
    template_name = 'nomina/catalogos/empleados/consulta_empleados.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(ConsultaEmpleados, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context