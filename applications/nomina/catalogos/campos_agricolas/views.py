from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.users.mixins import LoginAndActiveMixin, PermisoNomina
from .forms import FormularioCampos


class RegistrarCampos(LoginAndActiveMixin, PermisoNomina, CreateView):
    model = NomCampos
    form_class = FormularioCampos
    template_name = "nomina/catalogos/campos_agricolas/registro_campos.html"
    success_url = reverse_lazy('nomina:catalogos:campos:lista')
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
        context = super(RegistrarCampos, self).get_context_data(**kwargs)

        # Generamos el nuevo codigo correspondiente a esta compania
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        context['codigo_actual'] = codigo
        return context


class ListaCampos(LoginAndActiveMixin, PermisoNomina, ListView):
    model = NomCampos
    template_name = "nomina/catalogos/campos_agricolas/lista_campos.html"
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = {}
        campo_buscado = self.request.GET.get('campo_buscado')
        if campo_buscado is not None:
            context['lista_campos'] = NomCampos.objects.filter(nombre__icontains=campo_buscado)
        else:
            context['lista_campos'] = NomCampos.objects.all()

        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
