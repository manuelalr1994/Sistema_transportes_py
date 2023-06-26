from datetime import datetime, timedelta
import json

import pkgutil
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from applications.facturacion.procesos.asignar_factura.models import FletesFacturas, FletesFacturasRemisiones
from applications.facturacion.procesos.procesar_maquila.forms import FormularioFletesMaquilas

from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.facturacion.procesos.elaborar_remision.models import FletesMaquilas, FletesAbonos, FletesRemisiones

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

class AsignarFactura(LoginAndActiveMixin, PermisoFacturacion, TemplateView):
    template_name = 'facturacion/procesos/asignar_factura/factura_asignar.html'
    login_url = reverse_lazy('users_app:user_login')
    
    def get_context_data(request):
        context = {}
        lista_campos = NomCampos.objects.all()

        context['listado_campos'] = lista_campos
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class EstadoCuentaFacturas(LoginAndActiveMixin, PermisoFacturacion, TemplateView):
    template_name = 'facturacion/procesos/asignar_factura/estado_cuenta_facturas.html'
    login_url = reverse_lazy('users_app:user_login')

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
        return redirect('facturacion:procesos:asignar_factura:asignarFactura')

    def post(self, request):
        remision = FletesRemisiones.objects.get(pk=request.POST.get('remision'))
        codigo_factura = request.POST.get('codigo_factura')
        data = {}

        print(remision.importe)
        print(codigo_factura)

        if FletesFacturas.objects.filter(codigo=codigo_factura).exists():
            data['exitoso'] = False
            data['error'] = 'Ese codigo de factura ya existe'
            return JsonResponse(data)
        
        # Creamos la factura en la base de datos
        factura = FletesFacturas(codigo=codigo_factura, importe=remision.importe, fecha=datetime.today())
        factura.save()

        # Ligamos todas las remisiones vinculadas a esa factura
        factura.remisiones.add(remision)
        factura.save()

        # Asignamos valor true a facturada en remision
        remision.facturada = True
        remision.save()

        data['exitoso'] = True
        return JsonResponse(data)


# ------------------- CARGAS PARA PETICIONES AJAX -------------------------

def cargarListaRemisiones(request):

    if request.user.permisos_facturacion:
        context = {}
        template_name = 'facturacion/procesos/asignar_factura/cargar_lista_facturas.html'

        # Extraemos la informacion desde el metodo get
        campo_agricola = request.GET.get('campo_agricola')
        fecha_inicio = toDate(request.GET.get('fecha_inicio'))
        fecha_final = toDate(request.GET.get('fecha_final'))

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
        print(lista_final_ec)
        return render(request, template_name, context)
    else:
        return redirect('users_app:user_error')


def cargarRemision(request):

    if request.user.permisos_facturacion:
        model = FletesFacturas
        remision = request.GET.get('remision')
        remision = FletesRemisiones.objects.get(pk=remision)
        data = {}
        abono_dict = {}
        lista_abonos = FletesAbonos.objects.filter(remision=remision)
        lista_abonos_enviar = []  # Este tendra la forma necesaria para esr enviada

        # Conseguir informacion de la remision
        data['fecha'] = remision.fecha
        data['campo_agricola'] = remision.campo_agricola.nombre
        data['ubicacion'] = remision.campo_agricola.ubicacion.nombre

        # Generamos codigo de la factura
        try:
            codigo = int(model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(5, '0')
        except:
            codigo = "00001"

        data['codigo_factura'] = codigo

        # Conseguir la lista de abonos correspondiente
        for abono in lista_abonos:
            abono_dict['semana'] = str(abono.maquila.semana)
            abono_dict['fecha'] = abono.remision.fecha
            abono_dict['tipo'] = abono.tipo
            # ESTA FORMULA DE CALCULO DEL IMPORTE VA A PROVOCAR BUGS A FUTURO POR QUE NO SE TOMAN EN CUENTA TODOS LOS
            # SALDOS PREVIAMENTE REGISTRADOS !!!!!!
            abono_dict['importe'] = abono.maquila.importe_maquila - abono.saldo
            lista_abonos_enviar.append(abono_dict.copy())

        # Enviamos la informacion
        data['lista_abonos'] = lista_abonos_enviar
        return JsonResponse(data)
    else:
        return redirect('users_app:user_error')


def cargarDesglose(request):

    if request.user.permisos_facturacion:
        template_name = 'facturacion/procesos/asignar_factura/cargar_desglose_remision.html'
        data = {}
        remision = request.GET.get('remision')
        abono_dict = {}
        lista_abonos_dict = []

        # Conseguir informacion de la remision
        data['total'] = FletesRemisiones.objects.get(pk=remision).importe
        lista_abonos = FletesAbonos.objects.filter(remision=remision)

        for abono in lista_abonos:
            abono_dict['semana'] = abono.maquila.semana.semana
            if abono.tipo == "a":
                abono_dict['tipo'] = "Abono"
                # ERROR HAY QUE MEJORAR EL METODO DE CALCULO DE IMPORTE EN CASO DE ABONO
                abono_dict['importe'] = abono.maquila.importe_maquila - abono.saldo

            elif abono.tipo == "t":
                abono_dict['tipo'] = "Pago total"
                abono_dict['importe'] = abono.maquila.importe_maquila

            lista_abonos_dict.append(abono_dict.copy())
                

        # Enviamos la informacion
        data['lista_abonos'] = lista_abonos_dict
        return render(request, template_name, data)
    else:
        return redirect('users_app:user_error')
