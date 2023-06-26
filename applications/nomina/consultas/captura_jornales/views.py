import os
import datetime
from operator import truediv

from django.shortcuts import render
from django.http import JsonResponse, QueryDict, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from django.template.loader import get_template
from applications.nomina.catalogos.empleados.models import NomEmpleado
from weasyprint import HTML
from num2words import num2words

from applications.fletes.catalogos.camiones.models import Camiones
from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros
from applications.nomina.catalogos.cultivos.models import Cultivos, Variedad
from applications.nomina.catalogos.labores.models import NomLabores
from applications.nomina.catalogos.semanas.models import NomSemanas, NomTipoSemanas
from .models import NomJornales
from .forms import FormularioJornales

# NOTA IMPORTANTE: Cuando se hace referencia a "empresa" realmente hablamos del campo agricola
# solo que no cambiamos el nombre de la variable por que este cambio fue realizado cuando el modulo
# ya habia sido realizado, por eso se decidio dejarlo como empresa, para evitar los problemas que
# implica (el envio se realizara con el nombre empresa desde la peticion AJAX)

def semanaCerrada(semana, campo_agricola, tipo_semana):
    capturas = NomJornales.objects.filter(semana=semana, campo_agricola=campo_agricola, tipo_semana=tipo_semana).values_list('cerrada', flat=True).distinct()
    if len(capturas) < 1:
        return False
    elif all(capturas):
        return True
    else:
        return False

def toDate(fecha_string):
    fecha_string = fecha_string.split("/")
    fecha = datetime.datetime(int(fecha_string[2]), int(fecha_string[1]), int(fecha_string[0]))
    return fecha

# Create your views here.
# Create your views here.


# def ModificarCaptura(request):
#     template_name = "fletes/procesos/modificacion/mod_capturas.html"
#     data = {}
#     context = {}
#     context['form'] = FormularioJornada
#     context['dias_semana'] = []

#     # Generamos dias de la Semana para mostrarlos en el Template en las 
#     # id de los campos de la tabla
#     for i in range(7):
#         context['dias_semana'].append(i + 1)

#     # Definimos el metodo POST y el GET
#     if request.method == "POST":
#         capturas = []
#         capturas_dicts = {}


#         # Revisamos si todos los campos han sido llenados 
#         for key, value in request.POST.items():
#             if len(value) <= 0:
#                 data['error'] = 'Todos los campos deben ser llenados'
#                 data['exitoso'] = False
#                 return JsonResponse(data)

#         # Revisamos si la semana ya fue cerrada
#         campo_agricola = request.POST.getlist('empresas[]')[0]
#         semana = request.POST.get('semana')
#         tipo_semana = request.POST.get('tipo_semana')
#         if semanaCerrada(campo_agricola=campo_agricola, semana=semana, tipo_semana=tipo_semana):
#             data['error'] = 'Esta semana ya ha sido cerrada'
#             data['exitoso'] = False
#             return JsonResponse(data)

#         # Convertimos las listas del POST request a formularios
#         for i in range(len(request.POST.getlist('id_capturas[]'))):

#             fecha = toDate(request.POST.getlist('fechas[]')[i])

#             hora_entrada = float(request.POST.getlist('horas_entrada[]')[i])
#             hora_salida = float(request.POST.getlist('horas_salida[]')[i])

#             if hora_entrada < 0 or hora_entrada >= 24:
#                 data['error'] = 'Introduzca por favor solo horas validas'
#                 data['exitoso'] = False
#                 return JsonResponse(data)
#             elif hora_salida < 0 or hora_salida >= 24:
#                 data['error'] = 'Introduzca por favor solo horas validas'
#                 data['exitoso'] = False
#                 return JsonResponse(data)

#             captura_dict = {'campo_agricola':request.POST.getlist('empresas[]')[i], 'tipo_semana':request.POST.get('tipo_semana'),
#             'semana':request.POST.get('semana'), 'cuadrillero':request.POST.getlist('cuadrilleros[]')[i],
#             'cultivo':request.POST.getlist('cultivos[]')[i], 'variedad':request.POST.getlist('variedades[]')[i],
#             'labor':request.POST.getlist('labores[]')[i], 'camion':request.POST.get('camion'),
#             'fecha': fecha, 'hora_entrada':hora_entrada,
#             'hora_salida':hora_salida, 'costo_hra':request.POST.get('costo_hra'),
#             'total_hrs':request.POST.getlist('total_hrs[]')[i], 'importe':request.POST.getlist('importes[]')[i]}
#             captura_querydict = QueryDict('', mutable=True)
#             captura_querydict.update(captura_dict)
#             capturas_dicts[request.POST.getlist('id_capturas[]')[i]] = captura_dict
#             captura = FormularioJornada(captura_querydict)
#             capturas.append(captura)

#         # Corroboramos si todos las capturas son validas
#         for i in range(len(capturas)):
#             if not capturas[i].is_valid():

#                 data['error'] = capturas[i].errors.as_json()
#                 data['exitoso'] = False
#                 return JsonResponse(data)

#         # Hacemos la consulta de los elementos de la base de datos a modificar
#         id_camion = request.POST.get('camion')
#         id_semana = request.POST.get('semana')
#         id_empresa = request.POST.get('empresa_original')
#         capturas = NomJornales.objects.filter(camion=id_camion, semana=id_semana, campo_agricola=id_empresa).order_by('fecha')

#         # Actualizamos objetos captura y realizamos el bulk update
#         for captura in capturas:
#             captura.campo_agricola = NomCampos.objects.get(pk = capturas_dicts[""+str(captura.pk)]['campo_agricola'])
#             captura.tipo_semana = NomTipoSemanas.objects.get(pk = capturas_dicts[""+str(captura.pk)]['tipo_semana'])
#             captura.semana = NomSemanas.objects.get(pk = capturas_dicts[""+str(captura.pk)]['semana'])
#             captura.cuadrillero = NomCuadrilleros.objects.get(pk = capturas_dicts[""+str(captura.pk)]['cuadrillero'])
#             captura.cultivo = Cultivos.objects.get(pk = capturas_dicts[""+str(captura.pk)]['cultivo'])
#             captura.variedad = Variedad.objects.get(pk = capturas_dicts[""+str(captura.pk)]['variedad'])
#             captura.labor = NomLabores.objects.get(pk = capturas_dicts[""+str(captura.pk)]['labor'])
#             captura.camion = Camiones.objects.get(pk = capturas_dicts[""+str(captura.pk)]['camion'])
#             captura.fecha = capturas_dicts[""+str(captura.pk)]['fecha']
#             captura.hora_entrada = capturas_dicts[""+str(captura.pk)]['hora_entrada']
#             captura.hora_salida = capturas_dicts[""+str(captura.pk)]['hora_salida']
#             captura.costo_hra = capturas_dicts[""+str(captura.pk)]['costo_hra']
#             captura.total_hrs = capturas_dicts[""+str(captura.pk)]['total_hrs']
#             captura.importe = capturas_dicts[""+str(captura.pk)]['importe']

#         NomJornales.objects.bulk_update(capturas, ['campo_agricola', 'tipo_semana', 'semana',
#         'cuadrillero', 'cultivo', 'variedad', 'labor', 'camion', 'fecha', 'hora_entrada', 
#         'hora_salida', 'costo_hra', 'total_hrs', 'importe'])

#         data['exitoso'] = True
#         return JsonResponse(data)

#     else:  
#         return render(request, template_name, context)


def RegistrarCaptura(request):
    template_name = 'nomina/consultas/captura_jornales/captura_jornales.html'
    context = {}
    context['form'] = FormularioJornales
    context['dias_semana'] = []

    # Generamos dias de la Semana para mostrarlos en el Template en las 
    # id de los campos de la tabla
    for i in range(7):
        context['dias_semana'].append(i + 1)

    # Definimos acciones al recibir un POST request
    if request.method == "POST":
        data = {}
        capturas = []

        print(request.POST)

        # Revisamos si todos los campos han sido llenados 
        for key, value in request.POST.items():
            if len(value) <= 0:
                data['error'] = 'Todos los campos deben ser llenados'
                data['exitoso'] = False
                return JsonResponse(data)

        # Revisamos si la semana ya fue cerrada
        campo_agricola = request.POST.get('campo_agricola')
        semana = request.POST.get('semana')
        tipo_semana = request.POST.get('tipo_semana')

        if semanaCerrada(campo_agricola=campo_agricola, semana=semana, tipo_semana=tipo_semana):
            data['error'] = 'Esta semana ya ha sido cerrada'
            data['exitoso'] = False
            return JsonResponse(data)


        # Convertimos a formularios la informacion recabada del metodo POST
        # para su posterior validacion con el metodo is_valid()
        for i in range(len(request.POST.getlist('fechas[]'))):

            fecha = toDate(request.POST.getlist('fechas[]')[i])
            empleado = request.POST.get('empleado')

            if not NomJornales.objects.filter(fecha = fecha, empleado=empleado).exists():

                costo_hra_extra = NomEmpleado.objects.get(pk=empleado).campo_agricola.costo_hra_extra
                total_dinero_hrs_extra = float(request.POST.getlist('horas_extra[]')[i]) * float(costo_hra_extra)

                captura_dict = {'campo_agricola':request.POST.get('campo_agricola'), 'tipo_semana':request.POST.get('tipo_semana'),
                'semana':request.POST.get('semana'), 'cuadrillero':request.POST.get('cuadrillero'),
                'empleado':request.POST.get('empleado'), 'fecha': fecha, 'referencia':request.POST.get('referencia'),
                'temporada':request.POST.get('temporada'), 'labor':request.POST.get('labor'), 
                'total_dinero':request.POST.getlist('totales_dinero[]')[i], 'total_hrs_extra':request.POST.getlist('horas_extra[]')[i],
                'total_dinero_hrs_extra':total_dinero_hrs_extra}
                captura_querydict = QueryDict('', mutable=True)
                captura_querydict.update(captura_dict)
                captura = FormularioJornales(captura_querydict)
                capturas.append(captura)

        # Corroboramos si todos las capturas son validas
        for i in range(len(capturas)):
            print('bebe no aviso')
            if not capturas[i].is_valid():
                print('bebe solo avisa')
                data['errors'] = capturas[i].errors
                data['exitoso'] = False
                return JsonResponse(data)

        for i in range(len(capturas)):
            captura = NomJornales(**capturas[i].cleaned_data)
            captura.save()

        data['exitoso'] = True
        return JsonResponse(data)

    #Definimos Metodo GET
    else:
        return render(request, template_name, context)


def cargarDatosEmpleado(request):
    data = {}
    empleado_id = request.GET.get('empleado')
    empleado = NomEmpleado.objects.get(pk=empleado_id)
    data['cuenta'] = empleado.cuenta_banco
    data['no_tarjeta'] = empleado.num_tarjeta
    data['puesto'] = empleado.puesto
    data['salario'] = empleado.salario_base
    data['costo_hra_extra'] = empleado.campo_agricola.costo_hra_extra
    return JsonResponse(data)


# Esta vista se encarga de cargar los dias ya registrados del camion cuando se esté registrando una captura
def cargarDiasEmpleado(request):
    data = {}

    # Revisamos los campos necesarios fueron llenados
    for key, value in request.GET.items():
        if len(value) <= 0:
            data['error'] = 'Todos los campos deben ser llenados'
            data['exitoso'] = False
            return JsonResponse(data)

    # Extraemos datos del GET request
    campo_agricola = request.GET.get('campo_agricola')
    fecha_inicial = request.GET.get('fecha_inicial').split("-")
    fecha_final = request.GET.get('fecha_final').split("-")
    empleado = request.GET.get('empleado')

    # Transformamos las fechas en objetos tipo date
    fecha_inicial = datetime.datetime(int(fecha_inicial[0]), int(fecha_inicial[1]), int(fecha_inicial[2]))
    fecha_final = datetime.datetime(int(fecha_final[0]), int(fecha_final[1]), int(fecha_final[2]))

    # Revisamos si hay registros con los parametros para la consulta, para saber si existe lista_dias
    if NomJornales.objects.filter(campo_agricola=campo_agricola, empleado=empleado, fecha__range=(fecha_inicial, fecha_final)).exists():

        data['exitoso'] = True
        data['existe_lista_dias'] = True

        # Hacemos la consulta de las fechas en el rango que va desde la fecha inicial hasta la final
        consulta_dias = NomJornales.objects.filter(campo_agricola=campo_agricola, empleado=empleado, fecha__range=(fecha_inicial, fecha_final)).order_by('fecha')
        lista_dias = []
        diccionario_dia = {}

        # Estructuramos las informacion para ser enviada
        for dia in consulta_dias:

            diccionario_dia['fecha'] = dia.fecha
            diccionario_dia['total_dinero'] = dia.total_dinero
            diccionario_dia['total_hrs_extra'] = dia.total_hrs_extra

            # A la lista se añade una copia para evitar que todos los indices
            # referencien al mismo diccionario
            lista_dias.append(diccionario_dia.copy()) 

        data['lista_dias'] = lista_dias
        return JsonResponse(data)

    else:
        data['exitoso'] = True
        data['existe_lista_dias'] = False
        return JsonResponse(data)


# Verificamos que la semana seleccionada en el cierre de semanas este cerrada
def verificarSemanaCerrada(request):
    context = {}
    campo_agricola = request.GET.get("campo_agricola")
    tipo_semana = request.GET.get("tipo_semana")
    semana = request.GET.get("semana")

    capturas_cerradas = NomJornales.objects.filter(campo_agricola=campo_agricola, tipo_semana=tipo_semana, semana=semana).values_list('cerrada', flat=True)

    # Corroboramos que no haya ninguna captura no cerrada de la seleccion
    if all(capturas_cerradas) and len(capturas_cerradas) > 0:
        context['semana_cerrada'] = True
        context['mensaje_semana_cerrada'] = 'Esta semana ya ha sido cerrada'
        return JsonResponse(context)

    context['semana_cerrada'] = False
    return JsonResponse(context)


# # ----------------------------- REPORTES -----------------------------------

# class ReporteListadoCamiones(View):

#     def get(self, request, *args, **kwargs):

#         try:
#             context = {}

#             # Generamos el Contexto para el Template
#             diccionario_dias = {0:'lunes', 1:'martes', 2:'miercoles', 3:'jueves', 4:'viernes', 5:'sabado', 6:'domingo'}

#             empresa = int(request.GET.get('empresa'))
#             tipo_semana = int(request.GET.get('tipo_semana'))
#             semana = int(request.GET.get('semana'))

#             # Definimos las fecha, hora y numero de la cabecera
#             semana_query = NomSemanas.objects.get(pk=semana)
#             context["numero_semana"] = semana_query.semana
#             context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
#             context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
#             context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
#             context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")


#             lista_camiones = NomJornales.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).values_list('camion', flat=True).distinct()
#             lista_capturas = NomJornales.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).order_by('fecha')
#             lista_capturas_final = []
#             dict_captura = {}
#             total_general = 0 # Este llevara la suma de los totales de importe de todos los camiones
#             total_horas_general = 0 # Este llevara la suma de los totales de horas de todos los camiones
#             horas_totales = 0 # Este llevara el total de horas del camion
#             total_importe = 0 # Este llevara el importe total del camion

#             # Con la lista de camiones extraida, creamos diccionarios para cada camion
#             # con la informacion de las capturas de cada uno para esa semana
#             for camion in lista_camiones:

#                 # Inicializamos a 0 las horas trabajadas en todos los dias de la semana
#                 for dia in diccionario_dias.values():
#                     dict_captura[dia] = 0

#                 # Recorremos las capturas del camion actual y extraemos 
#                 # sus horas trabajadas y las horas por dia
#                 for captura in lista_capturas:
#                     if captura.camion.pk == camion:
#                         dict_captura['id'] = captura.camion.pk
#                         dict_captura['codigo'] = str(captura.camion.codigo).rjust(5, '0')
#                         dict_captura['nombre'] = captura.camion.nombre
#                         dia_semana_captura = diccionario_dias[captura.fecha.weekday()]
#                         dict_captura[dia_semana_captura] = captura.total_hrs
#                         horas_totales = round(horas_totales + captura.total_hrs, 2)
#                         total_importe = round((total_importe + (captura.camion.costo_hra * captura.total_hrs)), 2)

#                 dict_captura['horas'] = horas_totales
#                 dict_captura['sub_total'] = total_importe
#                 dict_captura['diesel'] = round(0, 2)
#                 dict_captura['comida'] = round(0, 2)
#                 dict_captura['total'] = total_importe
#                 total_general = total_general + total_importe
#                 total_horas_general = total_horas_general + horas_totales

#                 lista_capturas_final.append(dict_captura.copy())

#             context['lista_capturas'] = lista_capturas_final
#             context['nombre_reporte'] = "LISTADO GENERAL DE CAMIONES"
#             context['total_general'] = round(total_general, 2)
#             context['total_horas_general'] = round(total_horas_general, 2)
            
#             template = get_template("fletes/procesos/modificacion/reportes/reporte_listado_camiones.html")
#             html_template = template.render(context)
#             pdf = HTML(string=html_template).write_pdf()
#             return HttpResponse(pdf, content_type='application/pdf')
            
#         except:
#             pass

#         return HttpResponseRedirect(reverse_lazy('fletes:procesos:capturas_fleteras:modificar'))


# class ReporteBitacora(View):

#     def post(self, request, *args, **kwargs):

#         context = {}
#         dict_camion = {}

#         # --------- Generamos el Contexto para el Template ---------
#         camiones = request.POST.getlist('lang')
#         semana = int(request.POST.get('semana'))
#         lista_capturas_camion = []

#         # Hacemos la consulta de las capturas en base a la lista de camiones seleccionados y
#         # la semana a la que se hace referencia
#         for camion in camiones:
#             lista_capturas = NomJornales.objects.filter(camion=camion, semana=semana)
#             camion_query = Camiones.objects.get(pk=camion)

#             # Transformamos las fechas de los objetos FleJornadas en fechas string con el formato
#             # Tambien calculamos el Total de Horas y tambien el Total a Pagar
#             total_hrs = 0
#             total_pagar = 0
#             for captura in lista_capturas:
#                 captura.fecha = captura.fecha.strftime("%d/%m/%y")
#                 total_pagar = total_pagar + captura.importe
#                 total_hrs = total_hrs + captura.total_hrs

#             dict_camion["costo_hra"] = camion_query.costo_hra
#             dict_camion["compania_fletera"] = camion_query.compania_fletera
#             dict_camion["nombre"] = str(camion_query.codigo).rjust(5, '0') +" | "+str(camion_query.nombre)
#             dict_camion["lista_capturas"] = lista_capturas
#             dict_camion["total_hrs"] = total_hrs
#             dict_camion["total_pagar"] = total_pagar
#             dict_camion["total_pagar_palabras"] = num2words(total_pagar, lang="es").title()
#             dict_camion["total_hrs"] = total_hrs

#             lista_capturas_camion.append(dict_camion.copy())

        
#         context["lista_capturas_camion"] = lista_capturas_camion
        

#         # Definimos las fecha, hora y numero de la cabecera
#         semana_query = NomSemanas.objects.get(pk=semana)
#         context["nombre_reporte"] = "RECIBO DE PAGO"
#         context["numero_semana"] = semana_query.semana
#         context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
#         context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
#         context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
#         context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")

#         # Generamos el PDF
#         template = get_template("fletes/procesos/modificacion/reportes/reporte_bitacora.html")
#         html_template = template.render(context)
#         pdf = HTML(string=html_template).write_pdf()
#         return HttpResponse(pdf, content_type='application/pdf')

#         # try:
#         #     context = {}
#         #     dict_camion = {}

#         #     print("ENTRE PERO TRONE FLACOOOOOOOOOO")

#         #     # --------- Generamos el Contexto para el Template ---------
#         #     camiones = request.POST.getlist('lang')
#         #     semana = int(request.POST.get('semana'))
#         #     lista_capturas_camion = []

#         #     # Hacemos la consulta de las capturas en base a la lista de camiones seleccionados y
#         #     # la semana a la que se hace referencia
#         #     for camion in camiones:
#         #         lista_capturas = NomJornales.objects.filter(camion=camion, semana=semana)
#         #         camion_query = Camiones.objects.get(pk=camion)

#         #         # Transformamos las fechas de los objetos FleJornadas en fechas string con el formato
#         #         # Tambien calculamos el Total de Horas y tambien el Total a Pagar
#         #         total_hrs = 0
#         #         total_pagar = 0
#         #         for captura in lista_capturas:
#         #             captura.fecha = captura.fecha.strftime("%d/%m/%y")
#         #             total_pagar = total_pagar + captura.importe
#         #             total_hrs = total_hrs + captura.total_hrs

#         #         dict_camion["costo_hra"] = camion_query.costo_hra
#         #         dict_camion["compania_fletera"] = camion_query.compania_fletera
#         #         dict_camion["nombre"] = str(camion_query.codigo).rjust(5, '0') +" | "+str(camion_query.nombre)
#         #         dict_camion["lista_capturas"] = lista_capturas
#         #         dict_camion["total_hrs"] = total_hrs
#         #         dict_camion["total_pagar"] = total_pagar
#         #         dict_camion["total_pagar_palabras"] = num2words(total_pagar, lang="es").title()
#         #         dict_camion["total_hrs"] = total_hrs

#         #         lista_capturas_camion.append(dict_camion.copy())

            
#         #     context["lista_capturas_camion"] = lista_capturas_camion
            

#         #     # Definimos las fecha, hora y numero de la cabecera
#         #     semana_query = NomSemanas.objects.get(pk=semana)
#         #     context["nombre_reporte"] = "RECIBO DE PAGO"
#         #     context["numero_semana"] = semana_query.semana
#         #     context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
#         #     context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
#         #     context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
#         #     context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")

#         #     # Generamos el PDF
#         #     template = get_template("fletes/procesos/modificacion/reportes/reporte_bitacora.html")
#         #     html_template = template.render(context)
#         #     pdf = HTML(string=html_template).write_pdf()
#         #     return HttpResponse(pdf, content_type='application/pdf')
            
#         # except:
#         #     pass

#         # return HttpResponseRedirect(reverse_lazy('fletes:procesos:capturas_fleteras:modificar'))

#     # El metodo GET va a lidiar con el caso de que sea un reporte con una sola bitacora, llamada desde el boton "ver"
#     # la logica es exactamente la misma que en el metodo POST, solo que sin una lista
#     def get(self, request, *args, **kwargs):

#         try:
#             context = {}
#             lista_capturas_camion = []
#             dict_camion = {}

#             # --------- Generamos el Contexto para el Template ---------
#             camion = request.GET.get('camion')
#             semana = int(request.GET.get('semana'))

#             # Hacemos la consulta del camion especifico
#             lista_capturas = NomJornales.objects.filter(camion=camion, semana=semana)
#             camion_query = Camiones.objects.get(pk=camion)

#             # Transformamos las fechas de los objetos FleJornadas en fechas string con el formato
#             # Tambien calculamos el Total de Horas y tambien el Total a Pagar
#             total_hrs = 0
#             total_pagar = 0
#             for captura in lista_capturas:
#                 captura.fecha = captura.fecha.strftime("%d/%m/%y")
#                 total_pagar = total_pagar + captura.importe
#                 total_hrs = total_hrs + captura.total_hrs

#             dict_camion["costo_hra"] = camion_query.costo_hra
#             dict_camion["compania_fletera"] = camion_query.compania_fletera
#             dict_camion["nombre"] = str(camion_query.codigo).rjust(5, '0') +" | "+str(camion_query.nombre)
#             dict_camion["lista_capturas"] = lista_capturas
#             dict_camion["total_hrs"] = total_hrs
#             dict_camion["total_pagar"] = total_pagar
#             dict_camion["total_pagar_palabras"] = num2words(total_pagar, lang="es").title()
#             dict_camion["total_hrs"] = total_hrs

#             lista_capturas_camion.append(dict_camion.copy())

            
#             context["lista_capturas_camion"] = lista_capturas_camion
            

#             # Definimos las fecha, hora y numero de la cabecera
#             semana_query = NomSemanas.objects.get(pk=semana)
#             context["nombre_reporte"] = "RECIBO DE PAGO"
#             context["numero_semana"] = semana_query.semana
#             context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
#             context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
#             context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
#             context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")

#             # Generamos el PDF
#             template = get_template("fletes/procesos/modificacion/reportes/reporte_bitacora.html")
#             html_template = template.render(context)
#             pdf = HTML(string=html_template).write_pdf()
#             return HttpResponse(pdf, content_type='application/pdf')
            
#         except:
#             pass

#         return HttpResponseRedirect(reverse_lazy('fletes:procesos:capturas_fleteras:modificar'))