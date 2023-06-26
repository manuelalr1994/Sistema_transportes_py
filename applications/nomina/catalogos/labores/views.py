from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from applications.nomina.catalogos.labores.models import NomLabores
from applications.users.mixins import LoginAndActiveMixin, PermisoNomina

from .forms import FormularioLabores

class RegistrarLabores(LoginAndActiveMixin, PermisoNomina, CreateView):
    model = NomLabores
    form_class = FormularioLabores
    template_name = "nomina/catalogos/labores/registro_labor.html"
    success_url = reverse_lazy('nomina:catalogos:labores:lista')
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
        context = super(RegistrarLabores, self).get_context_data(**kwargs)

        # Generamos el nuevo codigo correspondiente a esta labor
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        context['codigo_actual'] = codigo
        return context


# Create your views here.
class ListaLabores(LoginAndActiveMixin, PermisoNomina, ListView):
    model = NomLabores
    template_name = "nomina/catalogos/labores/lista_labores.html"
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = {}
        labor_buscada = self.request.GET.get('labor_buscada')
        if labor_buscada is not None:
            context['lista_labores'] = NomLabores.objects.filter(nombre__icontains=labor_buscada)
        else:
            context['lista_labores'] = NomLabores.objects.all()

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

