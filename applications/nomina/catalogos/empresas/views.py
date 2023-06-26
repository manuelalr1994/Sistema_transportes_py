from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import forms
from applications.nomina.catalogos.empresas.models import NomEmpresas
from applications.nomina.catalogos.semanas.models import NomTipoSemanas
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from applications.users.mixins import LoginAndActiveMixin, PermisoNomina
#from applications.nomina.catalogos.ubicaciones.models import ubicaciones


# Modulo para crear empresas
class RegistrarEmpresas(LoginAndActiveMixin, PermisoNomina, CreateView):
    model = NomEmpresas
    form_class = forms.FormularioEmpresas
    template_name = 'nomina/catalogos/empresas/registro_empresas.html'
    success_url = reverse_lazy('nomina:catalogos:empresas:lista')
    login_url = reverse_lazy('users_app:user_login')

    def form_valid(self, form):
        # Generamos el nuevo codigo correspondiente a esta labor
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        #ubicacion = ubicaciones.objects.get(pk=self.request.COOKIES.get('ubicacion_usuario'))

        form.instance.codigo = codigo
        #form.instance.ubicacion = ubicacion
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrarEmpresas, self).get_context_data(**kwargs)
        consulta_tipos = NomTipoSemanas.objects.all()
        diccionario_tipos = {}

        for tipo in consulta_tipos:
            diccionario_tipos[tipo.tipo] = tipo.nombre
        
        # Generamos el nuevo codigo correspondiente a esta labor
        try:
            codigo = int(self.model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(3, '0')
        except:
            codigo = "001"

        context['codigo_actual'] = codigo
        context['diccionario_tipo_semanas'] = diccionario_tipos
        return context


# Modulo para mostrar lista de empresas (Elimina y Muestra)
class ListaEmpresas(LoginAndActiveMixin, PermisoNomina, ListView):
    model = NomEmpresas
    template_name = 'nomina/catalogos/empresas/empresas.html'
    login_url = reverse_lazy('users_app:user_login')
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}
        #ubicacion = ubicaciones.objects.get(pk=self.request.COOKIES.get('ubicacion_usuario'))

        empresa_buscada = self.request.GET.get('empresa_buscada')
        if empresa_buscada is not None:
            #print(ubicacion)
            context['lista_empresas'] = NomEmpresas.objects.filter(activo=True, nombre__icontains=empresa_buscada) #ubicacion=ubicacion)
            print(context['lista_empresas'])
        else:
            context['lista_empresas'] = NomEmpresas.objects.filter(activo=True,) #ubicacion=ubicacion)
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


# Consulta individual de Empresas
class ConsultarEmpresas(LoginAndActiveMixin, PermisoNomina, DetailView):
    model = NomEmpresas
    template_name = 'nomina/catalogos/empresas/consulta_empresas.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = super(ConsultarEmpresas, self).get_context_data(**kwargs)
        consulta_tipos = NomTipoSemanas.objects.all()
        diccionario_tipos = {}

        for tipo in consulta_tipos:
            diccionario_tipos[tipo.tipo] = tipo.nombre
        
        context['diccionario_tipo_semanas'] = diccionario_tipos
        context['pk'] = self.kwargs['pk']
        return context


# Modulo para Actualizar Empresas
class ActualizarEmpresas(LoginAndActiveMixin, PermisoNomina, UpdateView):
    model = NomEmpresas
    form_class = forms.FormularioEmpresas
    template_name = 'nomina/catalogos/empresas/registro_empresas.html'
    success_url = reverse_lazy('nomina:catalogos:empresas:lista')
    login_url = reverse_lazy('users_app:user_login')


# Modulo para Inactivar Empresas
class EliminarEmpresas(LoginAndActiveMixin, PermisoNomina, DeleteView):
    model = NomEmpresas
    template_name = 'nomina/catalogos/empresas/nomempresas_confirm_delete.html'
    login_url = reverse_lazy('users_app:user_login')

    def post(self, request, *args, **kwargs):
        object = self.model.objects.get(id = kwargs['pk'])
        object.activo = False
        object.save()
        return redirect('nomina:catalogos:empresas:lista')


'''
# Create your views here.
 

    # Funciones Aplicacion
    def juntar_diccionarios(lista_diccionarios):
        diccionarios_juntos = {}
        for diccionario in lista_diccionarios:
            diccionarios_juntos.update(diccionario)

    return diccionarios_juntos

    if request.method=="POST":

        registro_empresas_der_1 = forms.RegistroEmpresas_der_1(request.POST)
        registro_empresas_med_1 = forms.RegistroEmpresas_med_1(request.POST)
        registro_empresas_med_2 = forms.RegistroEmpresas_med_2(request.POST)
        registro_empresas_izq_1 = forms.RegistroEmpresas_izq_1(request.POST)
        registro_empresas_izq_2 = forms.RegistroEmpresas_izq_2(request.POST)

        if (registro_empresas_der_1.is_valid() and registro_empresas_med_1.is_valid() 
            and registro_empresas_med_2.is_valid() and registro_empresas_izq_1.is_valid() 
            and registro_empresas_izq_2.is_valid()):

            # Juntamos Diccionarios en Informacion Empresa
            lista_formularios = [registro_empresas_izq_1.cleaned_data, registro_empresas_med_1.cleaned_data,
                                registro_empresas_izq_2.cleaned_data, registro_empresas_med_2.cleaned_data,
                                registro_empresas_der_1.cleaned_data]

            informacion_empresa = juntar_diccionarios(lista_formularios)

            # Subimos Informacion a la Base de Datos
            instancia = empresas(**informacion_empresa)
            instancia.save()

            return redirect('lista_empresas')

    else:
        registro_empresas_der_1 = forms.RegistroEmpresas_der_1()
        registro_empresas_med_1 = forms.RegistroEmpresas_med_1()
        registro_empresas_med_2 = forms.RegistroEmpresas_med_2()
        registro_empresas_izq_1 = forms.RegistroEmpresas_izq_1()
        registro_empresas_izq_2 = forms.RegistroEmpresas_izq_2()

    return render(request, 'nomina/catalogos/empresas/registro_empresas.html', {"registro_empresas_der_1":registro_empresas_der_1, 
        "registro_empresas_izq_1":registro_empresas_izq_1, "registro_empresas_izq_2":registro_empresas_izq_2,
        "registro_empresas_med_1":registro_empresas_med_1, "registro_empresas_med_2":registro_empresas_med_2,})


def ActualizarEmpresa(request, id):

    if request.method=="POST":

        registro_empresas_der_1 = forms.RegistroEmpresas_der_1(request.POST)
        registro_empresas_med_1 = forms.RegistroEmpresas_med_1(request.POST)
        registro_empresas_med_2 = forms.RegistroEmpresas_med_2(request.POST)
        registro_empresas_izq_1 = forms.RegistroEmpresas_izq_1(request.POST)
        registro_empresas_izq_2 = forms.RegistroEmpresas_izq_2(request.POST)

        if (registro_empresas_der_1.is_valid() and registro_empresas_med_1.is_valid() 
            and registro_empresas_med_2.is_valid() and registro_empresas_izq_1.is_valid() 
            and registro_empresas_izq_2.is_valid()):

            # Juntamos Diccionarios en Informacion Empresa
            lista_formularios = [registro_empresas_izq_1.cleaned_data, registro_empresas_med_1.cleaned_data,
                                registro_empresas_izq_2.cleaned_data, registro_empresas_med_2.cleaned_data,
                                registro_empresas_der_1.cleaned_data]

            informacion_empresa = juntar_diccionarios(lista_formularios)

            # Subimos Informacion a la Base de Datos
            instancia = empresas(**informacion_empresa)
            instancia.save()

            return redirect('lista_empresas')

    else:
        informacion_empresa = empresas.objects.filter(id = id)
        informacion_empresa = informacion_empresa.values()
        informacion_empresa = informacion_empresa[0]

        registro_empresas_der_1 = forms.RegistroEmpresas_der_1(initial={'codigo','nombre', 'direccion', 'colonia', 'estado', 'rfc'})
        registro_empresas_med_1 = forms.RegistroEmpresas_med_1(initial={'ciudad','cp', 'reg_patronal'})
        registro_empresas_med_2 = forms.RegistroEmpresas_med_2(initial={'semana_de_pago', 'descuento_sindical'})
        registro_empresas_izq_1 = forms.RegistroEmpresas_izq_1(initial={'factor':informacion_empresa['factor'], 'bins', 'caja', 'ton'})
        registro_empresas_izq_2 = forms.RegistroEmpresas_izq_2(initial={'planta':informacion_empresa['planta'], 'linea':informacion_empresa['linea']})

    return render(request, 'nomina/catalogos/empresas/registro_empresas.html', {"registro_empresas_der_1":registro_empresas_der_1, 
        "registro_empresas_izq_1":registro_empresas_izq_1, "registro_empresas_izq_2":registro_empresas_izq_2,
        "registro_empresas_med_1":registro_empresas_med_1, "registro_empresas_med_2":registro_empresas_med_2,})
'''
'''


'''