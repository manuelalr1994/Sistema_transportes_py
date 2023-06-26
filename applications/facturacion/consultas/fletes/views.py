from datetime import datetime, timedelta
import json
from weasyprint import HTML
from num2words import num2words
from django.template.loader import get_template

import pkgutil
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from applications.facturacion.procesos.asignar_factura.models import FletesFacturas, FletesFacturasRemisiones
from applications.facturacion.procesos.procesar_maquila.forms import FormularioFletesMaquilas

from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.fletes.procesos.capturas_fleteras.models import FleJornada
from applications.facturacion.procesos.elaborar_remision.models import FletesMaquilas, FletesAbonos, FletesRemisiones
from applications.nomina.catalogos.semanas.models import NomSemanas

from applications.users.mixins import LoginAndActiveMixin, PermisoFacturacion
from django.urls import reverse_lazy


def toDate(fecha_string):
    fecha_string = fecha_string.split("-")
    fecha = datetime(int(fecha_string[0]), int(fecha_string[1]), int(fecha_string[2]))
    return fecha

def devolverFecha(registro):
    if hasattr(registro, 'fecha'):
        return registro.fecha
    elif hasattr(registro, 'semana'):
        return registro.semana.fecha_final
    return registro.fecha

def mezcla_maquilas_remisiones(lista_maquilas, lista_remisiones):
    lista_maquilas_remisiones = []
    for maquila in lista_maquilas:
        lista_maquilas_remisiones.append(maquila)
    
    for remision in lista_remisiones:
        lista_maquilas_remisiones.append(remision)

    lista_maquilas_remisiones.sort(key = devolverFecha)

    return lista_maquilas_remisiones


# Create your views here.
class ListaEstadoCuenta(TemplateView):
    template_name = 'facturacion/consulta/fletes/estado_cuenta/lista_estado_cuenta.html'

    def get_context_data(request):
        context = {}
        lista_campos = NomCampos.objects.all()

        context['listado_campos'] = lista_campos
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class EstadoCuenta(TemplateView):
    template_name = 'facturacion/consulta/fletes/estado_cuenta/estado_cuenta_facturas.html'

    def get(self, request):

        # Se revisa si el get contiene el campo agricola
        if request.GET.get('campo_agricola'):
            context = {}
            # anadir el try except para evitar problemas por malas llaves primarias en el get <-----
            try:
                context['campo_agricola'] = NomCampos.objects.get(pk = request.GET.get('campo_agricola'))
                context['lista_remisiones'] = FletesRemisiones.objects.filter(facturada=False, campo_agricola=request.GET.get('campo_agricola'))
                return render(request, self.template_name, context)
            except:
                return redirect('facturacion:procesos:asignar_factura:asignarFactura')

        # En caso de que no contenga campo, se redirecciona a la lista de campos para maquilar
        return redirect('facturacion:consultas:fletes:ListaEstadoCuenta')


class reporteEstadoCuenta(TemplateView):

    def get(self, request, *args, **kwargs):

        #try:
        context = {}

        # Generamos el Contexto para el Template
        diccionario_dias = {0:'lunes', 1:'martes', 2:'miercoles', 3:'jueves', 4:'viernes', 5:'sabado', 6:'domingo'}

        campo_agricola = int(request.GET.get('campo_agricola'))
        fecha_inicio = toDate(request.GET.get('fecha_inicio'))
        fecha_final = toDate(request.GET.get('fecha_final'))

        # Definimos las fecha, hora y numero de la cabecera
        context["numero_semana"] = "----"
        context["inicio"] = fecha_inicio.strftime("%d/%m/%y")
        context["cierre"] = fecha_final.strftime("%d/%m/%y")
        context["dia_reporte"] = datetime.now().strftime("%d/%m/%y")
        context["hora_reporte"] = datetime.now().strftime("%H:%M:%S")

        # ------ GENERAMOS LA LISTA DEL ESTADO DE CUENTA -------
        context = {}
        template_name = 'facturacion/consulta/fletes/estado_cuenta/reportes/reporte_estado_cuenta.html'

        # Consultamos la lista de maquilas y remisiones correspondientes a
        # los datos recibidos mediante el metodo get
        lista_maquilas = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial__range=[fecha_inicio, fecha_final], procesada = True).order_by('semana__fecha_final')
        lista_remisiones = FletesRemisiones.objects.filter(campo_agricola=campo_agricola, fecha__range=[fecha_inicio, fecha_final]).order_by('fecha')

        # Mezclamos la lista de maquilas y remisiones para ser mostradas
        # en el template
        lista_estado_cuenta = mezcla_maquilas_remisiones(lista_maquilas, lista_remisiones)

        # Mapeamos las maquilas en diccionarios para añadirles el saldo en la sumatoria
        diccionario_remision = {}
        diccionario_maquila = {}
        lista_final_ec = [] # Lista final estado cuenta
        for registro in lista_estado_cuenta:
            if hasattr(registro, 'fecha'):
                print(registro)
                if FletesFacturasRemisiones.objects.filter(remision=registro).exists():
                    factura = FletesFacturasRemisiones.objects.get(remision=registro)
                    diccionario_remision['factura'] = factura.factura.codigo
                    diccionario_remision['fecha_factura'] = factura.factura.fecha
                diccionario_remision['pk'] = registro.pk
                diccionario_remision['codigo'] = registro.codigo
                diccionario_remision['fecha_remision'] = registro.fecha
                diccionario_remision['facturada'] = registro.facturada
                diccionario_remision['importe'] = registro.importe
                lista_final_ec.append(diccionario_remision.copy())
            else:
                diccionario_maquila['pk'] = registro.pk
                diccionario_maquila['semana'] = registro.semana.semana
                diccionario_maquila['fecha_semana'] = str(registro.semana)
                diccionario_maquila['hrs_fletes'] = registro.hrs_fletes
                diccionario_maquila['costo_maquila'] = registro.costo_maquila
                diccionario_maquila['importe'] = registro.importe_maquila
                lista_final_ec.append(diccionario_maquila.copy())
        
        # ---------------- CALCULAMOS LOS SALDOS -------------------

        # Recuperamos los saldos hasta el momento
        limite_registros_pasados = fecha_inicio - timedelta(days=1)  # para el limite en el rango de los registros utilizados para la sumatoria inicial
        lista_maquilas_pasadas = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial__range=[datetime(2000, 1, 1), limite_registros_pasados], procesada = True).order_by('semana__fecha_final')
        lista_remisiones_pasadas = FletesRemisiones.objects.filter(campo_agricola=campo_agricola, fecha__range=[datetime(2000, 1, 1), limite_registros_pasados]).order_by('fecha')
        lista_sumatoria_inicial = mezcla_maquilas_remisiones(lista_maquilas_pasadas, lista_remisiones_pasadas)
        sumatoria_inicial = 0 # Sumatoria inicial, se calcula tomando la sumatoria del saldo previo al rango de fechas seleccionado
        
        for registro in lista_sumatoria_inicial:
            # Corroboramos si es remision o maquila y sumamos o restamos segun sea el caso
            if hasattr(registro, 'fecha'):
                sumatoria_inicial = sumatoria_inicial - registro.importe
            else:
                sumatoria_inicial = sumatoria_inicial + registro.importe_maquila

        # Calculamos el saldo de las remisiones y maquilas partiendo del saldo inicial previo
        saldo_actual = sumatoria_inicial
        for registro in lista_final_ec:
            if 'fecha_remision' in registro:
                saldo_actual = saldo_actual - registro['importe']
                registro['saldo'] = saldo_actual
            else:
                saldo_actual = saldo_actual + registro['importe']
                registro['saldo'] = saldo_actual

        context['lista_estado_cuenta'] = lista_final_ec

        # Generamos el template con los datos recabados
        template = get_template(template_name)
        html_template = template.render(context)
        pdf = HTML(string=html_template).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')
            
        #except:
        #    pass

        return HttpResponseRedirect(reverse_lazy('facturacion:consultas:fletes:EstadoCuenta'))
