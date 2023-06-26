from datetime import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from applications.facturacion.procesos.procesar_maquila.forms import FormularioFletesMaquilas

from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.facturacion.procesos.procesar_maquila.models import FletesMaquilas

from applications.users.mixins import LoginAndActiveMixin, PermisoFacturacion
from django.urls import reverse_lazy

def toDate(fecha_string):
    fecha_string = fecha_string.split("-")
    fecha = datetime(int(fecha_string[0]), int(fecha_string[1]), int(fecha_string[2]))
    return fecha


# Create your views here.

class ListadoProcesarMaquila(LoginAndActiveMixin, PermisoFacturacion, ListView):
    template_name = 'facturacion/procesos/procesar_maquila/lista_maquila.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = {}
        dict_campo_agricola = {}    # Guarda la informacion de cada campo, su nombre y si fue procesado
        lista_campos_agricola = []  # Guarda todos los dict_campo_agricolas para ser mostrados en la lista del template
        consulta_campos_agricola = NomCampos.objects.all()
        
        for campo in consulta_campos_agricola:
            # Guardamos el nombre del campo agricola actual y extraemos las maquilas relacionadas a este
            lista_fletes_maquilas = FletesMaquilas.objects.filter(campo_agricola=campo.pk).values_list('procesada', flat=True)
            dict_campo_agricola['campo_agricola'] = campo

            print(all(lista_fletes_maquilas))

            # Verificamos si ya fueron procesadas todas las maquilas del campo
            if all(lista_fletes_maquilas):
                dict_campo_agricola['procesado'] = True
            else:
                dict_campo_agricola['procesado'] = False

            # Guardamos en la lista de campos la informacion recabada de este campo
            lista_campos_agricola.append(dict_campo_agricola.copy())

        context['lista_campos_agricola'] = lista_campos_agricola
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ProcesarMaquila(LoginAndActiveMixin, PermisoFacturacion, TemplateView):
    template_name = 'facturacion/procesos/procesar_maquila/registrar_maquila.html' # Funcionamiento normal del get
    login_url = reverse_lazy('users_app:user_login')

    def get(self, request):

        # Se revisa si el get contiene el campo agricola
        if request.GET.get('campo_agricola'):
            context = {}
            # anadir el try except para evitar problemas por malas llaves primarias en el get <-----
            try:
                context['campo_agricola'] = NomCampos.objects.get(pk = request.GET.get('campo_agricola'))
                return render(self.request, self.template_name, context)
            except:
                return redirect('facturacion:procesos:procesar_maquila:lista')

        # En caso de que no contenga campo, se redirecciona a la lista de campos para maquilar
        return redirect('facturacion:procesos:procesar_maquila:lista')

    def post(self, request):
        context = {}

        # Recuperamos la maquila modificada
        maquila = FletesMaquilas.objects.get(pk=request.POST.get('maquila_id'))

        # Actualizamos la maquila que fue modificada
        # maquila.costo_maquila = request.POST.get('costo_maquila')
        # maquila.importe_maquila = request.POST.get('importe_maquila')
        # maquila.procesada = True
        formulario_maquila = FormularioFletesMaquilas(request.POST ,instance=maquila)
        print(formulario_maquila.is_valid())
        print(formulario_maquila.errors.as_data())

        if formulario_maquila.is_valid():
            formulario_maquila.save()
            context['exitoso'] = True
            return JsonResponse(context)

        else:
            print(maquila)
            print(formulario_maquila.errors.as_data())
            context['exitoso'] = False
            context['error'] = 'El formulario fue llenado de manera incorrecta, intente de nuevo por favor'
            return JsonResponse(context)


# ------------------- CARGAS PARA PETICIONES AJAX -------------------------
def cargarListaMaquilas(request):

    if request.user.permisos_facturacion:
        context = {}
        template_name = 'facturacion/procesos/procesar_maquila/cargar_lista_maquilas.html'
        campo_agricola = request.GET.get('campo_agricola')
        fecha_inicio = toDate(request.GET.get('fecha_inicio'))
        fecha_final = toDate(request.GET.get('fecha_final'))

        context['lista_maquilas'] = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial__range=[fecha_inicio, fecha_final]).order_by('semana')
        return render(request, template_name, context)
    else:
        return redirect('users_app:user_error')

def cargarMaquilaModal(request):
    if request.user.permisos_facturacion:
        maquila_id = request.GET.get('maquila')
        maquila_consulta = FletesMaquilas.objects.get(pk=maquila_id)
        maquila = {}
        
        maquila['campo_agricola'] = maquila_consulta.campo_agricola.nombre
        maquila['campo_agricola_id'] = maquila_consulta.campo_agricola.pk
        maquila['semana'] = str(maquila_consulta.semana)
        maquila['semana_id'] = maquila_consulta.semana.pk
        maquila['tipo_semana'] = str(maquila_consulta.tipo_semana)
        maquila['tipo_semana_id'] = maquila_consulta.tipo_semana.pk
        maquila['cant_carros'] = maquila_consulta.cant_carros
        maquila['hrs_fletes'] = maquila_consulta.hrs_fletes

        return JsonResponse(maquila)
    else:
        return redirect('users_app:user_error')

# ----------------------------- REPORTES -----------------------------------
def reporteListadoMaquila(request, **kwargs):
    template_name = 'facturacion/procesos/procesar_maquila/registrar_maquila.html'
    return render(request, template_name)
