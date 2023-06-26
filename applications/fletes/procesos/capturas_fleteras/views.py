import os
import datetime
from operator import truediv

from django.shortcuts import render
from django.http import JsonResponse, QueryDict, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from django.template.loader import get_template
from weasyprint import HTML
from num2words import num2words

from applications.fletes.catalogos.camiones.models import Camiones
from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras
from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros
from applications.nomina.catalogos.cultivos.models import Cultivos, Variedad
from applications.nomina.catalogos.labores.models import NomLabores
from applications.nomina.catalogos.semanas.models import NomSemanas, NomTipoSemanas
from .models import FleJornada
from .forms import FormularioJornada

# NOTA IMPORTANTE: Cuando se hace referencia a "empresa" realmente hablamos del campo agricola
# solo que no cambiamos el nombre de la variable por que este cambio fue realizado cuando el modulo
# ya habia sido realizado, por eso se decidio dejarlo como empresa, para evitar los problemas que
# implica (el envio se realizara con el nombre empresa desde la peticion AJAX)

def semanaCerrada(semana, campo_agricola, tipo_semana):
    capturas = FleJornada.objects.filter(semana=semana, campo_agricola=campo_agricola, tipo_semana=tipo_semana).values_list('cerrada', flat=True).distinct()
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


def ModificarCaptura(request):
    template_name = "fletes/procesos/modificacion/mod_capturas.html"
    data = {}
    context = {}
    context['form'] = FormularioJornada
    context['dias_semana'] = []

    # Generamos dias de la Semana para mostrarlos en el Template en las 
    # id de los campos de la tabla
    for i in range(7):
        context['dias_semana'].append(i + 1)

    # Definimos el metodo POST y el GET
    if request.method == "POST":
        capturas = []
        capturas_dicts = {}


        # Revisamos si todos los campos han sido llenados 
        for key, value in request.POST.items():
            if len(value) <= 0:
                data['error'] = 'Todos los campos deben ser llenados'
                data['exitoso'] = False
                return JsonResponse(data)

        # Revisamos si la semana ya fue cerrada
        campo_agricola = request.POST.getlist('empresas[]')[0]
        semana = request.POST.get('semana')
        tipo_semana = request.POST.get('tipo_semana')
        if semanaCerrada(campo_agricola=campo_agricola, semana=semana, tipo_semana=tipo_semana):
            data['error'] = 'Esta semana ya ha sido cerrada'
            data['exitoso'] = False
            return JsonResponse(data)

        # Convertimos las listas del POST request a formularios
        for i in range(len(request.POST.getlist('id_capturas[]'))):

            fecha = toDate(request.POST.getlist('fechas[]')[i])

            hora_entrada = float(request.POST.getlist('horas_entrada[]')[i])
            hora_salida = float(request.POST.getlist('horas_salida[]')[i])

            if hora_entrada < 0 or hora_entrada >= 24:
                data['error'] = 'Introduzca por favor solo horas validas'
                data['exitoso'] = False
                return JsonResponse(data)
            elif hora_salida < 0 or hora_salida >= 24:
                data['error'] = 'Introduzca por favor solo horas validas'
                data['exitoso'] = False
                return JsonResponse(data)

            captura_dict = {'campo_agricola':request.POST.getlist('empresas[]')[i], 'tipo_semana':request.POST.get('tipo_semana'),
            'semana':request.POST.get('semana'), 'cuadrillero':request.POST.getlist('cuadrilleros[]')[i],
            'cultivo':request.POST.getlist('cultivos[]')[i], 'variedad':request.POST.getlist('variedades[]')[i],
            'labor':request.POST.getlist('labores[]')[i], 'camion':request.POST.get('camion'),
            'fecha': fecha, 'hora_entrada':hora_entrada,
            'hora_salida':hora_salida, 'costo_hra':request.POST.get('costo_hra'),
            'total_hrs':request.POST.getlist('total_hrs[]')[i], 'importe':request.POST.getlist('importes[]')[i]}
            captura_querydict = QueryDict('', mutable=True)
            captura_querydict.update(captura_dict)
            capturas_dicts[request.POST.getlist('id_capturas[]')[i]] = captura_dict
            captura = FormularioJornada(captura_querydict)
            capturas.append(captura)

        # Corroboramos si todos las capturas son validas
        for i in range(len(capturas)):
            if not capturas[i].is_valid():

                data['error'] = capturas[i].errors.as_json()
                data['exitoso'] = False
                return JsonResponse(data)

        # Hacemos la consulta de los elementos de la base de datos a modificar
        id_camion = request.POST.get('camion')
        id_semana = request.POST.get('semana')
        id_empresa = request.POST.get('empresa_original')
        capturas = FleJornada.objects.filter(camion=id_camion, semana=id_semana, campo_agricola=id_empresa).order_by('fecha')

        # Actualizamos objetos captura y realizamos el bulk update
        for captura in capturas:
            captura.campo_agricola = NomCampos.objects.get(pk = capturas_dicts[""+str(captura.pk)]['campo_agricola'])
            captura.tipo_semana = NomTipoSemanas.objects.get(pk = capturas_dicts[""+str(captura.pk)]['tipo_semana'])
            captura.semana = NomSemanas.objects.get(pk = capturas_dicts[""+str(captura.pk)]['semana'])
            captura.cuadrillero = NomCuadrilleros.objects.get(pk = capturas_dicts[""+str(captura.pk)]['cuadrillero'])
            captura.cultivo = Cultivos.objects.get(pk = capturas_dicts[""+str(captura.pk)]['cultivo'])
            captura.variedad = Variedad.objects.get(pk = capturas_dicts[""+str(captura.pk)]['variedad'])
            captura.labor = NomLabores.objects.get(pk = capturas_dicts[""+str(captura.pk)]['labor'])
            captura.camion = Camiones.objects.get(pk = capturas_dicts[""+str(captura.pk)]['camion'])
            captura.fecha = capturas_dicts[""+str(captura.pk)]['fecha']
            captura.hora_entrada = capturas_dicts[""+str(captura.pk)]['hora_entrada']
            captura.hora_salida = capturas_dicts[""+str(captura.pk)]['hora_salida']
            captura.costo_hra = capturas_dicts[""+str(captura.pk)]['costo_hra']
            captura.total_hrs = capturas_dicts[""+str(captura.pk)]['total_hrs']
            captura.importe = capturas_dicts[""+str(captura.pk)]['importe']

        FleJornada.objects.bulk_update(capturas, ['campo_agricola', 'tipo_semana', 'semana',
        'cuadrillero', 'cultivo', 'variedad', 'labor', 'camion', 'fecha', 'hora_entrada', 
        'hora_salida', 'costo_hra', 'total_hrs', 'importe'])

        data['exitoso'] = True
        return JsonResponse(data)

    else:  
        return render(request, template_name, context)


def RegistrarCaptura(request):
    template_name = 'fletes/procesos/capturas_fleteras/registro_capturas_fleteras.html'
    context = {}
    context['form'] = FormularioJornada
    context['dias_semana'] = []

    # Generamos dias de la Semana para mostrarlos en el Template en las 
    # id de los campos de la tabla
    for i in range(7):
        context['dias_semana'].append(i + 1)

    # Definimos acciones al recibir un POST request
    if request.method == "POST":
        data = {}
        capturas = []

        # Revisamos si todos los campos han sido llenados 
        for key, value in request.POST.items():
            if len(value) <= 0:
                data['error'] = 'Todos los campos deben ser llenados'
                data['exitoso'] = False
                return JsonResponse(data)

        # Revisamos si la semana ya fue cerrada
        campo_agricola = request.POST.get('empresa')
        semana = request.POST.get('semana')
        tipo_semana = request.POST.get('tipo_semana')

        print(campo_agricola)
        print(semana)
        print(tipo_semana)

        print(semanaCerrada(campo_agricola=campo_agricola, semana=semana, tipo_semana=tipo_semana))

        if semanaCerrada(campo_agricola=campo_agricola, semana=semana, tipo_semana=tipo_semana):
            data['error'] = 'Esta semana ya ha sido cerrada'
            data['exitoso'] = False
            return JsonResponse(data)

        # Convertimos a formularios la informacion recabada del metodo POST
        # para su posterior validacion con el metodo is_valid()
        for i in range(len(request.POST.getlist('fechas[]'))):

            fecha = toDate(request.POST.getlist('fechas[]')[i])
            camion = request.POST.get('camion')

            if not FleJornada.objects.filter(fecha = fecha, camion=camion).exists():
            
                hora_entrada = float(request.POST.getlist('horas_entrada[]')[i])
                hora_salida = float(request.POST.getlist('horas_salida[]')[i])

                if hora_entrada < 0 or hora_entrada >= 24:
                    data['error'] = 'Introduzca por favor solo horas validas'
                    data['exitoso'] = False
                    return JsonResponse(data)
                elif hora_salida < 0 or hora_salida >= 24:
                    data['error'] = 'Introduzca por favor solo horas validas'
                    data['exitoso'] = False
                    return JsonResponse(data)

                captura_dict = {'campo_agricola':request.POST.get('empresa'), 'tipo_semana':request.POST.get('tipo_semana'),
                'semana':request.POST.get('semana'), 'cuadrillero':request.POST.get('cuadrillero'),
                'cultivo':request.POST.get('cultivo'), 'variedad':request.POST.get('variedad'),
                'labor':request.POST.get('labor'), 'camion':request.POST.get('camion'),
                'fecha': fecha, 'hora_entrada':request.POST.getlist('horas_entrada[]')[i],
                'hora_salida':request.POST.getlist('horas_salida[]')[i], 'costo_hra':request.POST.getlist('costos_hra[]')[i],
                'total_hrs':request.POST.getlist('total_hrs[]')[i], 'importe':request.POST.getlist('importes[]')[i]}
                captura_querydict = QueryDict('', mutable=True)
                captura_querydict.update(captura_dict)
                captura = FormularioJornada(captura_querydict)
                capturas.append(captura)

        # Corroboramos si todos las capturas son validas
        for i in range(len(capturas)):
            if not capturas[i].is_valid():
                data['errors'] = capturas[i].errors
                data['exitoso'] = False
                return JsonResponse(data)

        for i in range(len(capturas)):
            captura = FleJornada(**capturas[i].cleaned_data)
            captura.save()

        data['exitoso'] = True
        return JsonResponse(data)

    #Definimos Metodo GET
    else:
        return render(request, template_name, context)


# Cargas para peticiones AJAX
def cargarVariedad(request):
    cultivo_id = request.GET.get('cultivo')
    variedades = Variedad.objects.filter(id_cultivo=cultivo_id).order_by('nombre')
    return render(request, 'fletes/procesos/capturas_fleteras/cargar_variedad.html', {'variedades': variedades})


def cargarCuadrillero(request):
    empresa_id = request.GET.get('empresa')
    cuadrilleros = NomCuadrilleros.objects.filter(campo_agricola=empresa_id).order_by('nombre')
    return render(request, 'fletes/procesos/capturas_fleteras/cargar_cuadrillero.html', {'cuadrilleros': cuadrilleros})


def cargarSemana(request):
    tipo_semana_id = request.GET.get('tipo_semana')
    semanas = NomSemanas.objects.filter(tipo_semana=tipo_semana_id).order_by('semana')
    return render(request, 'fletes/procesos/capturas_fleteras/cargar_semana.html', {'semanas': semanas})


def cargarFecha(request):
    data = {}
    semana_id = request.GET.get('semana')
    fecha_inicial = NomSemanas.objects.get(id=semana_id).fecha_inicial
    fecha_final = NomSemanas.objects.get(id=semana_id).fecha_final
    data['fecha'] = str(fecha_inicial) + '   a   ' + str(fecha_final)
    return JsonResponse(data)


def cargarTipoSemana(request):
    data = {}
    empresa_id = request.GET.get('empresa')

    if len(empresa_id) > 0:
        tipos_semana = NomCampos.objects.get(id=empresa_id).tipos_semana.all()
        data['tipos_semana'] = tipos_semana
        data['exitoso'] = True
        return render(request, 'fletes/procesos/capturas_fleteras/cargar_tipo_semana.html', data)
    else:
        data['exitoso'] = False
        data['error'] = "Todos los campos deben ser llenados de manera valida"


def cargarInformacionCamion(request):
    data = {}
    camion_id = request.GET.get('camion')
    data['nombre_camion'] = Camiones.objects.get(pk=camion_id).nombre
    data['costo_hra_camion'] = Camiones.objects.get(pk=camion_id).costo_hra
    data['codigo_compania'] = Camiones.objects.get(pk=camion_id).compania_fletera.pk
    data['nombre_compania'] = Camiones.objects.get(pk=camion_id).compania_fletera.nombre
    return JsonResponse(data)


def cargarListaCapturas(request):
    data = {}
    diccionario_dias = {0:'lunes', 1:'martes', 2:'miercoles', 3:'jueves', 4:'viernes', 5:'sabado', 6:'domingo'}

    empresa = int(request.GET.get('empresa'))
    tipo_semana = int(request.GET.get('tipo_semana'))
    semana = int(request.GET.get('semana'))

    lista_camiones = FleJornada.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).values_list('camion', flat=True).distinct()
    lista_capturas = FleJornada.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).order_by('fecha')
    data['semana_cerrada'] = FleJornada.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).values_list('cerrada', flat=True)[0]
    lista_capturas_final = []
    dict_captura = {}
    horas_totales = 0
    total_importe = 0

    # Con la lista de camiones extraida, creamos diccionarios para cada camion
    # con la informacion de las capturas de cada uno para esa semana
    for camion in lista_camiones:

        horas_totales = 0
        total_importe = 0

        # Inicializamos a 0 las horas trabajadas en todos los dias de la semana
        for dia in diccionario_dias.values():
            dict_captura[dia] = 0

        # Recorremos las capturas del camion actual y extraemos 
        # sus horas trabajadas y las horas por dia
        for captura in lista_capturas:
            if captura.camion.pk == camion:
                dict_captura['id'] = captura.camion.pk
                dict_captura['codigo'] = captura.camion.codigo
                dict_captura['nombre'] = captura.camion.nombre
                dia_semana_captura = diccionario_dias[captura.fecha.weekday()]
                dict_captura[dia_semana_captura] = captura.total_hrs
                horas_totales = round(horas_totales + captura.total_hrs, 2)
                total_importe = round((total_importe + (captura.camion.costo_hra * captura.total_hrs)), 2)

        dict_captura['horas'] = horas_totales
        dict_captura['sub_total'] = total_importe
        dict_captura['diesel'] = 0.00
        dict_captura['comida'] = 0.00
        dict_captura['total'] = total_importe

        lista_capturas_final.append(dict_captura.copy())

    data['lista_capturas'] = lista_capturas_final
    return render(request, 'fletes/procesos/modificacion/cargar_capturas_fleteras.html', data)


# Esta vista se encarga de cargar los dias ya registrados del camion cuando se esté registrando una captura
def cargarDiasCamion(request):
    data = {}

    # Revisamos los campos necesarios fueron llenados
    for key, value in request.GET.items():
        if len(value) <= 0:
            data['error'] = 'Todos los campos deben ser llenados'
            data['exitoso'] = False
            return JsonResponse(data)

    # Extraemos datos del GET request
    camion = request.GET.get('camion')
    fecha_inicial = request.GET.get('fecha_inicial').split("-")
    fecha_final = request.GET.get('fecha_final').split("-")

    # Transformamos las fechas en objetos tipo date
    fecha_inicial = datetime.datetime(int(fecha_inicial[0]), int(fecha_inicial[1]), int(fecha_inicial[2]))
    fecha_final = datetime.datetime(int(fecha_final[0]), int(fecha_final[1]), int(fecha_final[2]))

    # Revisamos si hay registros con los parametros para la consulta, para saber si existe lista_dias
    if FleJornada.objects.filter(camion=camion, fecha__range=(fecha_inicial, fecha_final)).exists():

        data['exitoso'] = True
        data['existe_lista_dias'] = True

        # Hacemos la consulta de las fechas en el rango que va desde la fecha inicial hasta la final
        consulta_dias = FleJornada.objects.filter(camion=camion, fecha__range=(fecha_inicial, fecha_final)).order_by('fecha')
        lista_dias = []
        diccionario_dia = {}

        # Estructuramos las informacion para ser enviada
        for dia in consulta_dias:

            diccionario_dia['fecha'] = dia.fecha
            diccionario_dia['entrada'] = dia.hora_entrada
            diccionario_dia['salida'] = dia.hora_salida
            diccionario_dia['costo'] = dia.costo_hra
            diccionario_dia['hrs_totales'] = dia.total_hrs
            diccionario_dia['importe'] = dia.importe

            # A la lista se añade una copia para evitar que todos los indices
            # referencien al mismo diccionario
            lista_dias.append(diccionario_dia.copy()) 

        data['lista_dias'] = lista_dias
        return JsonResponse(data)

    else:
        data['exitoso'] = True
        data['existe_lista_dias'] = False
        return JsonResponse(data)

    
def cargarCaptura(request):
    data = {}
    dict_captura = {}
    lista_capturas = {}
    informacion_camion = {}

    dias_semana = {0:'Lunes', 1:'Martes', 2:'Miércoles', 3:'Jueves', 4:'Viernes', 5:'Sábado', 6:'Domingo'}

    id_empresa = request.GET.get('empresa')
    id_camion = request.GET.get('camion')
    id_semana = request.GET.get('semana')
    capturas = FleJornada.objects.filter(camion=id_camion, semana=id_semana, campo_agricola = id_empresa).order_by('fecha')
    camion = Camiones.objects.get(pk = id_camion)

    # Guardamos la informacion del camion para ser enviada
    informacion_camion['id'] = camion.pk
    informacion_camion['codigo'] = camion.codigo
    informacion_camion['nombre'] = camion.nombre
    informacion_camion['costo_hra'] = camion.costo_hra

    # Realizamos la lista de capturas
    indice = 1
    for captura in capturas:
        dict_captura['id_captura'] = captura.pk
        dict_captura['dia'] = dias_semana[captura.fecha.weekday()]
        dict_captura['campo_agricola'] = captura.campo_agricola.pk
        dict_captura['tipo_semana'] = captura.tipo_semana.pk
        dict_captura['semana'] = captura.semana.pk
        dict_captura['cuadrillero'] = captura.cuadrillero.pk
        dict_captura['cultivo'] = captura.cultivo.pk
        dict_captura['variedad'] = captura.variedad.pk
        dict_captura['labor'] = captura.labor.pk
        dict_captura['camion'] = captura.camion.pk
        dict_captura['fecha'] = captura.fecha.strftime("%d/%m/%Y")
        dict_captura['hora_entrada'] = captura.hora_entrada
        dict_captura['hora_salida'] = captura.hora_salida
        dict_captura['costo_hra'] = captura.costo_hra
        dict_captura['total_hrs'] = captura.total_hrs
        dict_captura['importe'] = captura.importe
        dict_captura['cerrada'] = captura.cerrada

        lista_capturas[indice] = dict_captura.copy()
        indice += 1


    # Extraemos de la base de datos todas las opciones del campo empresa para mostrarlas en html
    empresas = NomCampos.objects.all()
    empresas_html = ""
    for empresa in empresas:
        empresas_html = empresas_html + "<option value="+str(empresa.pk)+">"+str(empresa)+"</option>"

    # Extraemos de la base de datos todas las opciones del campo plantacion para mostrarlas en html
    cultivos = Cultivos.objects.all()
    cultivos_html = ""
    for cultivo in cultivos:
        cultivos_html = cultivos_html + "<option value="+str(cultivo.pk)+">"+str(cultivo)+"</option>"

    # Extraemos de la base de datos todas las opciones del campo labor para mostrarlas en html
    labores = NomLabores.objects.all()
    labores_html = ""
    for labor in labores:
        labores_html = labores_html + "<option value="+str(labor.pk)+">"+str(labor)+"</option>"

    # Revisamos si estas capturas ya han sido cerradas
    semana_cerrada = lista_capturas[1]['cerrada']

    # Mandar informacion de regreso al AJAX request
    data['labores_html'] = labores_html
    data['empresas_html'] = empresas_html
    data['cultivos_html'] = cultivos_html
    data['lista_capturas'] = lista_capturas
    data['cant_capturas'] = indice
    data['camion'] = informacion_camion
    data['semana_cerrada'] = semana_cerrada
    return JsonResponse(data)


# Verificamos que la semana seleccionada en el cierre de semanas este cerrada
def verificarSemanaCerrada(request):
    context = {}
    campo_agricola = request.GET.get("campo_agricola")
    tipo_semana = request.GET.get("tipo_semana")
    semana = request.GET.get("semana")

    capturas_cerradas = FleJornada.objects.filter(campo_agricola=campo_agricola, tipo_semana=tipo_semana, semana=semana).values_list('cerrada', flat=True)

    # Corroboramos que no haya ninguna captura no cerrada de la seleccion
    if all(capturas_cerradas) and len(capturas_cerradas) > 0:
        context['semana_cerrada'] = True
        context['mensaje_semana_cerrada'] = 'Esta semana ya ha sido cerrada'
        return JsonResponse(context)

    context['semana_cerrada'] = False
    return JsonResponse(context)


# ----------------------------- REPORTES -----------------------------------

class ReporteListadoCamiones(View):

    def get(self, request, *args, **kwargs):

        try:
            context = {}

            # Generamos el Contexto para el Template
            diccionario_dias = {0:'lunes', 1:'martes', 2:'miercoles', 3:'jueves', 4:'viernes', 5:'sabado', 6:'domingo'}

            empresa = int(request.GET.get('empresa'))
            tipo_semana = int(request.GET.get('tipo_semana'))
            semana = int(request.GET.get('semana'))

            # Definimos las fecha, hora y numero de la cabecera
            semana_query = NomSemanas.objects.get(pk=semana)
            context["numero_semana"] = semana_query.semana
            context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
            context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
            context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
            context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")


            lista_camiones = FleJornada.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).values_list('camion', flat=True).distinct()
            lista_capturas = FleJornada.objects.filter(campo_agricola=empresa, tipo_semana=tipo_semana, semana=semana).order_by('fecha')
            lista_capturas_final = []
            dict_captura = {}
            total_general = 0 # Este llevara la suma de los totales de importe de todos los camiones
            total_horas_general = 0 # Este llevara la suma de los totales de horas de todos los camiones
            horas_totales = 0 # Este llevara el total de horas del camion
            total_importe = 0 # Este llevara el importe total del camion

            # Con la lista de camiones extraida, creamos diccionarios para cada camion
            # con la informacion de las capturas de cada uno para esa semana
            for camion in lista_camiones:

                # Inicializamos a 0 las horas trabajadas en todos los dias de la semana
                for dia in diccionario_dias.values():
                    dict_captura[dia] = 0

                # Recorremos las capturas del camion actual y extraemos 
                # sus horas trabajadas y las horas por dia
                for captura in lista_capturas:
                    if captura.camion.pk == camion:
                        dict_captura['id'] = captura.camion.pk
                        dict_captura['codigo'] = str(captura.camion.codigo).rjust(5, '0')
                        dict_captura['nombre'] = captura.camion.nombre
                        dia_semana_captura = diccionario_dias[captura.fecha.weekday()]
                        dict_captura[dia_semana_captura] = captura.total_hrs
                        horas_totales = round(horas_totales + captura.total_hrs, 2)
                        total_importe = round((total_importe + (captura.camion.costo_hra * captura.total_hrs)), 2)

                dict_captura['horas'] = horas_totales
                dict_captura['sub_total'] = total_importe
                dict_captura['diesel'] = round(0, 2)
                dict_captura['comida'] = round(0, 2)
                dict_captura['total'] = total_importe
                total_general = total_general + total_importe
                total_horas_general = total_horas_general + horas_totales

                lista_capturas_final.append(dict_captura.copy())

            context['lista_capturas'] = lista_capturas_final
            context['nombre_reporte'] = "LISTADO GENERAL DE CAMIONES"
            context['total_general'] = round(total_general, 2)
            context['total_horas_general'] = round(total_horas_general, 2)
            
            template = get_template("fletes/procesos/modificacion/reportes/reporte_listado_camiones.html")
            html_template = template.render(context)
            pdf = HTML(string=html_template).write_pdf()
            return HttpResponse(pdf, content_type='application/pdf')
            
        except:
            pass

        return HttpResponseRedirect(reverse_lazy('fletes:procesos:capturas_fleteras:modificar'))


class ReporteBitacora(View):

    def post(self, request, *args, **kwargs):

        context = {}
        dict_camion = {}

        # --------- Generamos el Contexto para el Template ---------
        camiones = request.POST.getlist('lang')
        semana = int(request.POST.get('semana'))
        lista_capturas_camion = []

        # Hacemos la consulta de las capturas en base a la lista de camiones seleccionados y
        # la semana a la que se hace referencia
        for camion in camiones:
            lista_capturas = FleJornada.objects.filter(camion=camion, semana=semana)
            camion_query = Camiones.objects.get(pk=camion)

            # Transformamos las fechas de los objetos FleJornadas en fechas string con el formato
            # Tambien calculamos el Total de Horas y tambien el Total a Pagar
            total_hrs = 0
            total_pagar = 0
            for captura in lista_capturas:
                captura.fecha = captura.fecha.strftime("%d/%m/%y")
                total_pagar = total_pagar + captura.importe
                total_hrs = total_hrs + captura.total_hrs

            dict_camion["costo_hra"] = camion_query.costo_hra
            dict_camion["compania_fletera"] = camion_query.compania_fletera
            dict_camion["nombre"] = str(camion_query.codigo).rjust(5, '0') +" | "+str(camion_query.nombre)
            dict_camion["lista_capturas"] = lista_capturas
            dict_camion["total_hrs"] = total_hrs
            dict_camion["total_pagar"] = total_pagar
            dict_camion["total_pagar_palabras"] = num2words(total_pagar, lang="es").title()
            dict_camion["total_hrs"] = total_hrs

            lista_capturas_camion.append(dict_camion.copy())

        
        context["lista_capturas_camion"] = lista_capturas_camion
        

        # Definimos las fecha, hora y numero de la cabecera
        semana_query = NomSemanas.objects.get(pk=semana)
        context["nombre_reporte"] = "RECIBO DE PAGO"
        context["numero_semana"] = semana_query.semana
        context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
        context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
        context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
        context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")

        # Generamos el PDF
        template = get_template("fletes/procesos/modificacion/reportes/reporte_bitacora.html")
        html_template = template.render(context)
        pdf = HTML(string=html_template).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')

        # try:
        #     context = {}
        #     dict_camion = {}

        #     print("ENTRE PERO TRONE FLACOOOOOOOOOO")

        #     # --------- Generamos el Contexto para el Template ---------
        #     camiones = request.POST.getlist('lang')
        #     semana = int(request.POST.get('semana'))
        #     lista_capturas_camion = []

        #     # Hacemos la consulta de las capturas en base a la lista de camiones seleccionados y
        #     # la semana a la que se hace referencia
        #     for camion in camiones:
        #         lista_capturas = FleJornada.objects.filter(camion=camion, semana=semana)
        #         camion_query = Camiones.objects.get(pk=camion)

        #         # Transformamos las fechas de los objetos FleJornadas en fechas string con el formato
        #         # Tambien calculamos el Total de Horas y tambien el Total a Pagar
        #         total_hrs = 0
        #         total_pagar = 0
        #         for captura in lista_capturas:
        #             captura.fecha = captura.fecha.strftime("%d/%m/%y")
        #             total_pagar = total_pagar + captura.importe
        #             total_hrs = total_hrs + captura.total_hrs

        #         dict_camion["costo_hra"] = camion_query.costo_hra
        #         dict_camion["compania_fletera"] = camion_query.compania_fletera
        #         dict_camion["nombre"] = str(camion_query.codigo).rjust(5, '0') +" | "+str(camion_query.nombre)
        #         dict_camion["lista_capturas"] = lista_capturas
        #         dict_camion["total_hrs"] = total_hrs
        #         dict_camion["total_pagar"] = total_pagar
        #         dict_camion["total_pagar_palabras"] = num2words(total_pagar, lang="es").title()
        #         dict_camion["total_hrs"] = total_hrs

        #         lista_capturas_camion.append(dict_camion.copy())

            
        #     context["lista_capturas_camion"] = lista_capturas_camion
            

        #     # Definimos las fecha, hora y numero de la cabecera
        #     semana_query = NomSemanas.objects.get(pk=semana)
        #     context["nombre_reporte"] = "RECIBO DE PAGO"
        #     context["numero_semana"] = semana_query.semana
        #     context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
        #     context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
        #     context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
        #     context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")

        #     # Generamos el PDF
        #     template = get_template("fletes/procesos/modificacion/reportes/reporte_bitacora.html")
        #     html_template = template.render(context)
        #     pdf = HTML(string=html_template).write_pdf()
        #     return HttpResponse(pdf, content_type='application/pdf')
            
        # except:
        #     pass

        # return HttpResponseRedirect(reverse_lazy('fletes:procesos:capturas_fleteras:modificar'))

    # El metodo GET va a lidiar con el caso de que sea un reporte con una sola bitacora, llamada desde el boton "ver"
    # la logica es exactamente la misma que en el metodo POST, solo que sin una lista
    def get(self, request, *args, **kwargs):

        try:
            context = {}
            lista_capturas_camion = []
            dict_camion = {}

            # --------- Generamos el Contexto para el Template ---------
            camion = request.GET.get('camion')
            semana = int(request.GET.get('semana'))

            # Hacemos la consulta del camion especifico
            lista_capturas = FleJornada.objects.filter(camion=camion, semana=semana)
            camion_query = Camiones.objects.get(pk=camion)

            # Transformamos las fechas de los objetos FleJornadas en fechas string con el formato
            # Tambien calculamos el Total de Horas y tambien el Total a Pagar
            total_hrs = 0
            total_pagar = 0
            for captura in lista_capturas:
                captura.fecha = captura.fecha.strftime("%d/%m/%y")
                total_pagar = total_pagar + captura.importe
                total_hrs = total_hrs + captura.total_hrs

            dict_camion["costo_hra"] = camion_query.costo_hra
            dict_camion["compania_fletera"] = camion_query.compania_fletera
            dict_camion["nombre"] = str(camion_query.codigo).rjust(5, '0') +" | "+str(camion_query.nombre)
            dict_camion["lista_capturas"] = lista_capturas
            dict_camion["total_hrs"] = total_hrs
            dict_camion["total_pagar"] = total_pagar
            dict_camion["total_pagar_palabras"] = num2words(total_pagar, lang="es").title()
            dict_camion["total_hrs"] = total_hrs

            lista_capturas_camion.append(dict_camion.copy())

            
            context["lista_capturas_camion"] = lista_capturas_camion
            

            # Definimos las fecha, hora y numero de la cabecera
            semana_query = NomSemanas.objects.get(pk=semana)
            context["nombre_reporte"] = "RECIBO DE PAGO"
            context["numero_semana"] = semana_query.semana
            context["inicio"] = semana_query.fecha_inicial.strftime("%d/%m/%y")
            context["cierre"] = semana_query.fecha_final.strftime("%d/%m/%y")
            context["dia_reporte"] = datetime.datetime.now().strftime("%d/%m/%y")
            context["hora_reporte"] = datetime.datetime.now().strftime("%H:%M:%S")

            # Generamos el PDF
            template = get_template("fletes/procesos/modificacion/reportes/reporte_bitacora.html")
            html_template = template.render(context)
            pdf = HTML(string=html_template).write_pdf()
            return HttpResponse(pdf, content_type='application/pdf')
            
        except:
            pass

        return HttpResponseRedirect(reverse_lazy('fletes:procesos:capturas_fleteras:modificar'))