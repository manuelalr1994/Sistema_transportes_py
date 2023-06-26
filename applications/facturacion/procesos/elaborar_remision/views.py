from datetime import datetime, timedelta
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from applications.facturacion.procesos.procesar_maquila.forms import FormularioFletesMaquilas

from applications.nomina.catalogos.campos_agricolas.models import NomCampos
from applications.facturacion.procesos.procesar_maquila.models import FletesMaquilas
from applications.facturacion.procesos.elaborar_remision.models import FletesAbonos, FletesRemisiones

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

# def mezcla_maquilas_remisiones(lista_maquilas, lista_remisiones):
#     lista_maquilas_remisiones = []
#     print('DESDE DENTRO MEZCLA MAQUILAS')
#     print(lista_maquilas)
#     print('DESDE DENTRO MEZCLA REMISIONES')
#     print(lista_remisiones)

#     if len(lista_remisiones) > 0:
#         contador = 0 # Para saber que numero es el objeto actual

#         # Recorremos la lista de remisiones y vamos comparando su fecha con las de las maquilas
#         # para saber en que punto la vamos a acomodar, para que queden acomodadas por fecha
#         for remision in lista_remisiones:
#             contador = contador + 1
#             for maquila in lista_maquilas:
#                 print(maquila.semana.fecha_final)
#                 print(remision.fecha)
#                 print(maquila.semana.fecha_final < remision.fecha)
#                 if maquila.semana.fecha_final < remision.fecha:
#                     lista_maquilas_remisiones.append(maquila)
#                     print('maquila')
#                     print(maquila)
#                 elif maquila.semana.fecha_final > remision.fecha:
#                     if contador == len(lista_remisiones):
#                         print('remision desde remision final')
#                         lista_maquilas_remisiones.append(remision)
#                         contador = contador + 1
#                     elif contador < len(lista_remisiones):
#                         print('remision desde remision en medio')
#                         lista_maquilas_remisiones.append(remision)
#                         break
#                     else:
#                         lista_maquilas_remisiones.append(maquila)
#                 else:
#                     print('maquila desde gana maquila')
#                     lista_maquilas_remisiones.append(maquila)
        
#         return lista_maquilas_remisiones

#     return lista_maquilas


# Create your views here.

class ListadoRemision(LoginAndActiveMixin, PermisoFacturacion, TemplateView):
    template_name = 'facturacion/procesos/elaborar_remision/remision.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        context = {}
        lista_campos_agricola = NomCampos.objects.all()

        context['lista_campos_agricola'] = lista_campos_agricola
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class EstadoCuentaRemision(LoginAndActiveMixin, PermisoFacturacion, TemplateView):
    template_name = 'facturacion/procesos/elaborar_remision/estado_cuenta_remision.html'
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
                return redirect('facturacion:procesos:elaborar_remision:lista')

        # En caso de que no contenga campo, se redirecciona a la lista de campos para maquilar
        return redirect('facturacion:procesos:elaborar_remision:lista')

    def post(self, request):

        context = {}
        json_string = request.POST.get('json')
        data = json.loads(json_string)

        print(data['fecha'])
        data['fecha'] = toDate(data['fecha'])

        # Damos de alta la remision
        campo_agricola = NomCampos.objects.get(pk=data['campo_agricola'])
        remision = FletesRemisiones(codigo=data['codigo_remision'], campo_agricola=campo_agricola, fecha=data['fecha'], importe=data['importe'])
        remision.save()

        # Creamos los abonos correspondientes
        lista_abonos = data['lista_abonos']
        remision_asignada = FletesRemisiones.objects.get(codigo=data['codigo_remision'])

        for abono in lista_abonos:
            maquila = FletesMaquilas.objects.get(pk=abono['id'])

            # t = total_pagado   a = abono
            if(abono['tipo_abono'] == "Pago Total"):
                tipo = 't'
            else:
                tipo = 'a'

            instancia_abono = FletesAbonos(campo_agricola=campo_agricola, remision=remision_asignada,
                                            maquila=maquila, saldo=abono['saldo'], tipo=tipo)
            instancia_abono.save()

        context['exitoso'] = True
        return JsonResponse(context)


# ------------------- CARGAS PARA PETICIONES AJAX -------------------------

def cargarListaRemisiones(request):

    if request.user.permisos_facturacion:
        context = {}
        template_name = 'facturacion/procesos/elaborar_remision/cargar_lista_remisiones.html'

        # Extraemos la informacion desde el metodo get
        campo_agricola = request.GET.get('campo_agricola')
        print(request.GET.get('fecha_inicio'))
        print(request.GET.get('fecha_final'))
        fecha_inicio = toDate(request.GET.get('fecha_inicio'))
        fecha_final = toDate(request.GET.get('fecha_final'))

        # Consultamos la lista de maquilas y remisiones correspondientes a
        # los datos recibidos mediante el metodo get
        lista_maquilas = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial__range=[fecha_inicio, fecha_final], procesada = True).order_by('semana__fecha_final')
        lista_remisiones = FletesRemisiones.objects.filter(campo_agricola=campo_agricola, fecha__range=[fecha_inicio, fecha_final]).order_by('fecha')

        print('lista_maquilas <<<<<<')
        print(lista_maquilas)

        print('lista_remisiones <<<<<<')
        print(lista_remisiones)

        # Mezclamos la lista de maquilas y remisiones para ser mostradas
        # en el template
        lista_estado_cuenta = mezcla_maquilas_remisiones(lista_maquilas, lista_remisiones)

        # Mapeamos las maquilas en diccionarios para añadirles el saldo en la sumatoria
        diccionario_remision = {}
        diccionario_maquila = {}
        lista_final_ec = [] # Lista final estado cuenta
        for registro in lista_estado_cuenta:
            if hasattr(registro, 'fecha'):
                diccionario_remision['pk'] = registro.pk
                diccionario_remision['codigo'] = registro.codigo
                diccionario_remision['fecha'] = registro.fecha
                diccionario_remision['importe'] = registro.importe
                print(diccionario_remision)
                lista_final_ec.append(diccionario_remision.copy())
            else:
                diccionario_maquila['pk'] = registro.pk
                diccionario_maquila['semana'] = registro.semana.semana
                diccionario_maquila['fecha_semana'] = str(registro.semana)
                diccionario_maquila['hrs_fletes'] = registro.hrs_fletes
                diccionario_maquila['costo_maquila'] = registro.costo_maquila
                diccionario_maquila['importe'] = registro.importe_maquila
                print('maquila')
                print(diccionario_maquila)
                lista_final_ec.append(diccionario_maquila.copy())
        
        # ---------------- CALCULAMOS LOS SALDOS -------------------

        # Recuperamos los saldos hasta el momento
        
        lista_maquilas_pasadas = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial__range=[datetime(2000, 1, 1), fecha_inicio], procesada = True).order_by('semana__fecha_final')
        lista_remisiones_pasadas = FletesRemisiones.objects.filter(campo_agricola=campo_agricola, fecha__range=[datetime(2000, 1, 1), fecha_inicio]).order_by('fecha')
        lista_sumatoria_inicial = mezcla_maquilas_remisiones(lista_maquilas_pasadas, lista_remisiones_pasadas)
        sumatoria_inicial = 0 # Sumatoria inicial, se calcula tomando la sumatoria del saldo previo al rango de fechas seleccionado

        print('REGISTRO DE SUMATORIA INICIAAAALLLL')
        print(lista_sumatoria_inicial)

        for registro in lista_sumatoria_inicial:
            # Corroboramos si es remision o maquila y sumamos o restamos segun sea el caso
            print(str(registro) + "REGISTRO IMPORTEEEE")
            if hasattr(registro, 'fecha'):
                sumatoria_inicial = sumatoria_inicial - registro.importe
            else:
                sumatoria_inicial = sumatoria_inicial + registro.importe_maquila
            print(sumatoria_inicial)

        print(str(sumatoria_inicial)+" <<<<<<< CHEEEEEEEEEETTT")

        # Calculamos el saldo de las remisiones y maquilas partiendo del saldo inicial previo
        saldo_actual = sumatoria_inicial
        for registro in lista_final_ec:
            print(str(sumatoria_inicial)+" EPAAAAAAAAAAAAA")
            if 'fecha' in registro:
                saldo_actual = saldo_actual - registro['importe']
                print('DESDE LA REMISION MI NIñO')
                print(str(saldo_actual)+"<---------------")
                registro['saldo'] = saldo_actual
            else:
                saldo_actual = saldo_actual + registro['importe']
                print('DESDE LA MAQUILA MI NIñO')
                print(str(saldo_actual)+"<---------------")
                registro['saldo'] = saldo_actual

        print(lista_final_ec)
        context['lista_estado_cuenta'] = lista_final_ec
        context['sumatoria_inicial'] = sumatoria_inicial
        return render(request, template_name, context)
    else:
        return redirect('users_app:user_error')


# Cargar la informacion para el modal de generar remision
def cargarCampoAgricola(request):

    if request.user.permisos_facturacion:
        data = {}
        campo_agricola_dict = {}
        campo_agricola = NomCampos.objects.get(pk = request.GET.get('campo_agricola'))
        model = FletesRemisiones

        # Generamos codigo de la remision
        try:
            codigo = int(model.objects.latest("id").codigo)
            codigo = str(codigo + 1).rjust(5, '0')
        except:
            codigo = "00001"

        campo_agricola_dict['codigo_remision'] = codigo
        campo_agricola_dict['campo_agricola_id'] = campo_agricola.pk
        campo_agricola_dict['campo_agricola'] = campo_agricola.nombre
        campo_agricola_dict['ubicacion_id'] = campo_agricola.ubicacion.pk
        campo_agricola_dict['ubicacion'] = campo_agricola.ubicacion.nombre

        data['campo_agricola'] = campo_agricola_dict
        return JsonResponse(data)
    else:
        return redirect('users_app:user_error')

def cargarSemanasRemision(request):

    if request.user.permisos_facturacion:
        data = {}
        campo_agricola = request.GET.get('campo_agricola')
        cantidad_abono = float(request.GET.get('cantidad_abono'))
        lista_abonos = FletesAbonos.objects.filter(campo_agricola=campo_agricola)
        lista_maquilas_abonadas = []

        print(str(len(lista_abonos))+" <---------------- sex")

        if len(lista_abonos) > 0:
            # Se busca el ultimo por id por que los abonos se almacenan de manera consecutiva y el id se incrementa
            # de la misma manera, por ende el id mas grande va a ser el ultimo
            ultimo_abono = FletesAbonos.objects.filter(campo_agricola=campo_agricola).latest('id')
            fecha_inicial = ultimo_abono.maquila.semana.fecha_inicial
            semana_abonada = {} # Este guardara la informacion de cada semana y el tipo de abono que se le hizo

            # Si el ultimo abono es del tipo abonado, se trata primero el saldo pendiente de ese 
            # abono y luego se sigue
            if ultimo_abono.tipo == 'a':

                # Se hace el abono al saldo pendiente primero y despues se continua con lo demas
                if cantidad_abono >= ultimo_abono.saldo:
                    semana_abonada["id"] = ultimo_abono.maquila.pk
                    semana_abonada["no_semana"] = ultimo_abono.maquila.semana.semana
                    semana_abonada["fechas"] = str(ultimo_abono.maquila.semana)
                    semana_abonada["tipo_abono"] = "Pago Total"
                    semana_abonada["importe_abonado"] = float(ultimo_abono.saldo)
                    semana_abonada["saldo"] = 0
                    lista_maquilas_abonadas.append(semana_abonada.copy())
                    cantidad_abono = cantidad_abono - float(ultimo_abono.saldo)
                    
                elif cantidad_abono < ultimo_abono.saldo:
                    semana_abonada["id"] = ultimo_abono.maquila.pk
                    semana_abonada["no_semana"] = ultimo_abono.maquila.semana.semana
                    semana_abonada["fechas"] = str(ultimo_abono.maquila.semana)
                    semana_abonada["tipo_abono"] = "Abono"
                    semana_abonada["importe_abonado"] = cantidad_abono
                    semana_abonada["saldo"] = float(ultimo_abono.maquila.importe_maquila) - cantidad_abono
                    lista_maquilas_abonadas.append(semana_abonada.copy())
                    cantidad_abono = 0

                # Se sigue realizando la iteracion hasta que la cantidad del abono es 0
                maquila = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial = fecha_inicial)
                fecha_inicial = fecha_inicial + timedelta(days=7)

                while(cantidad_abono > 0):

                    # Si la cantidad de abono sigue siendo mayor a 0 y ya no hay maquilas restantes
                    # se tiene que tratar la situacion
                    try:
                        maquila = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial = fecha_inicial)[0]
                    except:
                        data = {}
                        data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
                        return JsonResponse(data)

                    if cantidad_abono >= maquila.importe_maquila:
                        semana_abonada["id"] = maquila.pk
                        semana_abonada["no_semana"] = maquila.semana.semana
                        semana_abonada["fechas"] = str(maquila.semana)
                        semana_abonada["tipo_abono"] = "Pago Total"
                        semana_abonada["importe_abonado"] = float(maquila.importe_maquila)
                        semana_abonada["saldo"] = 0
                        lista_maquilas_abonadas.append(semana_abonada.copy())
                        cantidad_abono = cantidad_abono - float(maquila.importe_maquila)
                        
                    elif cantidad_abono < maquila.importe_maquila:
                        semana_abonada["id"] = maquila.pk
                        semana_abonada["no_semana"] = maquila.semana.semana
                        semana_abonada["fechas"] = str(maquila.semana)
                        semana_abonada["tipo_abono"] = "Abono"
                        semana_abonada["importe_abonado"] = cantidad_abono
                        semana_abonada["saldo"] = float(maquila.importe_maquila) - cantidad_abono
                        lista_maquilas_abonadas.append(semana_abonada.copy())
                        cantidad_abono = 0

                    fecha_inicial = fecha_inicial + timedelta(days=7)

                data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
                return JsonResponse(data)

            # Si el ultimo abono es del tipo total pagado, se inicia desde la siguiente semana a esa
            else:
                fecha_inicial = fecha_inicial + timedelta(days=7)

                while(cantidad_abono > 0):

                    # Si la cantidad de abono sigue siendo mayor a 0 y ya no hay maquilas restantes
                    # se tiene que tratar la situacion
                    try:
                        maquila = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial = fecha_inicial)[0]
                    except:
                        data = {}
                        data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
                        return JsonResponse(data)

                    if cantidad_abono >= maquila.importe_maquila:
                        semana_abonada["id"] = maquila.pk
                        semana_abonada["no_semana"] = maquila.semana.semana
                        semana_abonada["fechas"] = str(maquila.semana)
                        semana_abonada["tipo_abono"] = "Pago Total"
                        semana_abonada["importe_abonado"] = maquila.importe_maquila
                        semana_abonada["saldo"] = 0
                        lista_maquilas_abonadas.append(semana_abonada.copy())
                        cantidad_abono = cantidad_abono - float(maquila.importe_maquila)
                        
                    elif cantidad_abono < maquila.importe_maquila:
                        semana_abonada["id"] = maquila.pk
                        semana_abonada["no_semana"] = maquila.semana.semana
                        semana_abonada["fechas"] = str(maquila.semana)
                        semana_abonada["tipo_abono"] = "Abono"
                        semana_abonada["importe_abonado"] = cantidad_abono
                        semana_abonada["saldo"] = float(maquila.importe_maquila) - cantidad_abono
                        lista_maquilas_abonadas.append(semana_abonada.copy())
                        cantidad_abono = 0

                    fecha_inicial = fecha_inicial + timedelta(days=7)

                data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
                return JsonResponse(data)

        else:

            # Se verifica que exista alguna maquila, si no, se regresa la lista vacia
            try:
                primer_maquila = FletesMaquilas.objects.filter(campo_agricola=campo_agricola).earliest('semana__fecha_final')
            except:
                data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
                return JsonResponse(data)

            fecha_inicial = primer_maquila.semana.fecha_inicial
            semana_abonada = {} # Este guardara la informacion de cada semana y el tipo de abono que se le hizo
                                # este diccionario luego se ira añadiendo a la lista representando cada semana
            
            while(cantidad_abono > 0):

                # Si la cantidad de abono sigue siendo mayor a 0 y ya no hay maquilas restantes
                # se tiene que tratar la situacion
                try:
                    maquila = FletesMaquilas.objects.filter(campo_agricola=campo_agricola, semana__fecha_inicial = fecha_inicial)[0]
                except:
                    data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
                    return JsonResponse(data)

                if cantidad_abono >= maquila.importe_maquila:
                    semana_abonada["id"] = maquila.pk
                    semana_abonada["no_semana"] = maquila.semana.semana
                    semana_abonada["fechas"] = str(maquila.semana)
                    semana_abonada["tipo_abono"] = "Pago Total"
                    semana_abonada["importe_abonado"] = maquila.importe_maquila
                    semana_abonada["saldo"] = 0
                    lista_maquilas_abonadas.append(semana_abonada.copy())
                    cantidad_abono = cantidad_abono - float(maquila.importe_maquila)
                    
                elif cantidad_abono < maquila.importe_maquila:
                    semana_abonada["id"] = maquila.pk
                    semana_abonada["no_semana"] = maquila.semana.semana
                    semana_abonada["fechas"] = str(maquila.semana)
                    semana_abonada["tipo_abono"] = "Abono"
                    semana_abonada["importe_abonado"] = cantidad_abono
                    semana_abonada["saldo"] = float(maquila.importe_maquila) - cantidad_abono
                    lista_maquilas_abonadas.append(semana_abonada.copy())
                    cantidad_abono = 0

                fecha_inicial = fecha_inicial + timedelta(days=7)
            
            data['lista_maquilas_abonadas'] = lista_maquilas_abonadas
            return JsonResponse(data)
    else:
        return redirect('users_app:user_error')
        

    # Corroboramos si la lista esta vacia
        # Si esta vacia agarramos la semana mas vieja y de ahi partimos

    # Else en caso de que la lista no este vacia
        # Corroboramos si quedo un abono pendiente en la ultima
            # Agarramos esa ultima con abono y partimos de ahi
        # Else en caso de que no haya abono pendiente
            # Partimos de la siguiente semana a esa


def cargarDesglose(request):

    if request.user.permisos_facturacion:
        template_name = 'facturacion/procesos/elaborar_remision/cargar_desglose_remision.html'
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


# def cargarMaquilaModal(request):
#     maquila_id = request.GET.get('maquila')
#     maquila_consulta = FletesMaquilas.objects.get(pk=maquila_id)
#     maquila = {}
    
#     maquila['campo_agricola'] = maquila_consulta.campo_agricola.nombre
#     maquila['campo_agricola_id'] = maquila_consulta.campo_agricola.pk
#     maquila['semana'] = str(maquila_consulta.semana)
#     maquila['semana_id'] = maquila_consulta.semana.pk
#     maquila['tipo_semana'] = str(maquila_consulta.tipo_semana)
#     maquila['tipo_semana_id'] = maquila_consulta.tipo_semana.pk
#     maquila['cant_carros'] = maquila_consulta.cant_carros
#     maquila['hrs_fletes'] = maquila_consulta.hrs_fletes

#     return JsonResponse(maquila)
