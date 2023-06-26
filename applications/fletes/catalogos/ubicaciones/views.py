from django.shortcuts import render, redirect, reverse
from django.http import QueryDict
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import FormularioUbicaciones
from applications.nomina.catalogos.ubicaciones.models import ubicaciones
from applications.users.mixins import LoginAndActiveMixin, PermisoFletes

# Create your views here.
class ListaUbicaciones(LoginAndActiveMixin, PermisoFletes, View):
    model = ubicaciones
    form_class = FormularioUbicaciones
    template_name = 'fletes/catalogos/ubicaciones/lista_ubicaciones.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class
        ubicacion_buscada = self.request.GET.get('ubicacion_buscada')
        if ubicacion_buscada is not None:
            context['lista_ubicaciones'] = self.model.objects.filter(nombre__icontains=ubicacion_buscada)
        else:
            context['lista_ubicaciones'] = self.model.objects.all()
            
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):

        # Asignamos un codigo
        try:
            codigo = str(int(self.model.objects.latest('id').codigo) + 1).rjust(3, '0')
        except:
            codigo = "001"

        # Realizamos la instancia del formulario
        ubicacion_dict = {'codigo':codigo, 'nombre':request.POST.get('nombre')}
        ubicacion_querydict = QueryDict('', mutable=True)
        ubicacion_querydict.update(ubicacion_dict)
        form = self.form_class(ubicacion_querydict)

        if form.is_valid():
            ubicacion = self.model(**form.cleaned_data)
            ubicacion.save()
        
        return redirect('fletes:catalogos:ubicaciones:lista')