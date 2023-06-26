from collections import Counter
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import NomTipoSemanas, NomSemanas
from datetime import datetime
from django.views.generic import View
from applications.users.mixins import LoginAndActiveMixin, PermisoNomina

# ------ Funciones Propias ---------

# Validamos las fechas que nos llegan del cliente
def validar_fecha(fecha):

    # Nos cercioramos que la fecha contiene / separando las secciones
    if fecha.count('/') != 2:
        return False
    
    fecha_elementos = fecha.split('/')

    # Nos cercioramos que los elementos de fecha son numeros
    try:
        dia = int(fecha_elementos[0])
        mes = int(fecha_elementos[1])
        anio = int(fecha_elementos[2])

    except:
        return False

    # Nos cercioramos que los elementos de fecha son validos para una fecha
    if anio < datetime.today().year:
        return False
    elif mes <= 0 or mes > 12:
        return False
    elif dia <= 0 or dia > 31:
        return False

    return True

# Generamos el nombre del tipo a guardar en la base de datos segun una fecha inicial y una final
def generador_nombre_tipo(fecha_inicial, fecha_final):
    diccionario_dias = {0:"LUNES", 1:"MARTES", 2:"MIERCOLES", 3:"JUEVES", 4:"VIERNES", 5:"SABADO", 6:"DOMINGO"}
    dia_inicial = diccionario_dias[fecha_inicial.weekday()]
    dia_final = diccionario_dias[fecha_final.weekday()]
    return dia_inicial +" A "+ dia_final

# Transformamos las fechas en forma de strings a objetos fecha de Python
def string_a_datetime(fecha_string):
    fecha_separada = fecha_string.split('/')
    fecha = datetime(int(fecha_separada[2]), int(fecha_separada[1]), int(fecha_separada[0]))
    return fecha

# Recibimos una lista con elementos string los cuales son numeros y devolvemos una lista con estos
# elementos transformados a enteros
def lista_string_a_entero(lista_strings):
    lista_transformada = []
    for cadena in lista_strings:
        entero = int(cadena)
        lista_transformada.append(entero)

    return lista_transformada

def validar_listas_fechas(lista_fecha_inicial, lista_fecha_final, lista_id):
    contador = 0
    error = ''

    for fecha in lista_fecha_inicial:
        if validar_fecha(fecha) == False:
            error = '<p style="color: red;">Las fechas son invalidas</p>'
            break
        elif validar_fecha(lista_fecha_final[contador]) == False:
            error = '<p style="color: red;">Las fechas son invalidas</p>'
            break
        elif int(lista_id[contador]) < 1 or int(lista_id[contador]) > 52:
            error = '<p style="color: red;">Las ID de las semanas son invalidas</p>'
            break
        else:
            contador = contador + 1
    
    return error
        


#-----------Views-----------------------

# Create your views here.
def RegistrarSemanas(request):

    if request.user.permisos_nomina:
        contexto = {}
        consulta_tipos = NomTipoSemanas.objects.all()
        diccionario_tipos = {}

        for tipo in consulta_tipos:
            diccionario_tipos[tipo.tipo] = tipo.nombre

        contexto['diccionario_tipos'] = diccionario_tipos

        # Usamos el metodo POST para subir registros a la base de datos
        # este metodo POST se manda llamar con un boton submit o
        # desde una solicitud AJAX
        if request.method=="POST":

            tipo = request.POST.get('tipo')
            error = ''

            # Nos cercioramos que no se halla introducido un tipo invalido
            if tipo == None:
                error = '<p style="color: red;">Introduzca un tipo por favor</p>'
                contexto['error'] = error
                contexto['exitoso'] = False
                return JsonResponse(contexto)
            elif not tipo.isnumeric():
                error = '<p style="color: red;">Introduzca un tipo valido por favor</p>'
                contexto['error'] = error
                contexto['exitoso'] = False
                return JsonResponse(contexto)
            else:
                tipo = int(tipo)

            if tipo < 1 or tipo > 7 :
                error = '<p style="color: red;">No se pueden dar de alta más de 7 tipos de semana</p>'
                contexto['error'] = error
                contexto['exitoso'] = False
                return JsonResponse(contexto)

            lista_fecha_inicial = request.POST.getlist('lista_fecha_inicial[]')
            lista_fecha_final = request.POST.getlist('lista_fecha_final[]')
            lista_id = lista_string_a_entero(request.POST.getlist('lista_id[]'))

            # Validamos listas de fechas
            error = validar_listas_fechas(lista_fecha_inicial, lista_fecha_final, lista_id)

            # Extraemos una fecha inicial y final de las listas fechas para usarlas
            # de referencia en el nombramiento (LUNES A VIERNES, MARTES A VIERNES, ETC)
            fecha_inicial = string_a_datetime(lista_fecha_inicial[0])
            fecha_final = string_a_datetime(lista_fecha_final[0])
            nombre = generador_nombre_tipo(fecha_inicial, fecha_final)

            lista_tipos = NomTipoSemanas.objects.all().values_list('tipo', flat = True)
            lista_nombres = NomTipoSemanas.objects.all().values_list('nombre', flat = True)

            if tipo in lista_tipos:
                nombre_tipo = str(NomTipoSemanas.objects.get(tipo = tipo).nombre)
                lista_semanas_tipo = NomSemanas.objects.filter(anio = datetime.today().year, tipo_semana = tipo).values_list('tipo_semana', flat = True)
                if nombre != nombre_tipo:
                    error = '<p style="color: red;">El tipo '+ str(tipo) +' va de '+ nombre_tipo.lower() +'</p>'
                    contexto['error'] = error
                    contexto['exitoso'] = False
                    return JsonResponse(contexto)
                elif len(lista_semanas_tipo) > 0:
                    error = '<p style="color: red;">Ya existe el tipo '+ str(tipo) +' para el año '+ str(datetime.today().year) +'</p>'
                    contexto['error'] = error
                    contexto['exitoso'] = False
                    return JsonResponse(contexto)
            else:
                if nombre in lista_nombres:
                    tipo_del_nombre = NomTipoSemanas.objects.get(nombre = nombre).tipo
                    error = '<p style="color: red;">'+ str(nombre).lower() +' está asignado al tipo '+ str(tipo_del_nombre) +'</p>'
                    contexto['error'] = error
                    contexto['exitoso'] = False
                    return JsonResponse(contexto)
                else:
                    instancia_tipo = NomTipoSemanas(nombre=nombre, tipo=tipo)
                    instancia_tipo.save()

            # Mostramos error si las id_semana se repiten
            apariciones_ids = Counter(lista_id)
            for apariciones_id in apariciones_ids:
                if apariciones_ids[apariciones_id] > 1:
                    error = '<p style="color: red;">Las ID de las semanas no se pueden repetir</p>'
                    break

            # En caso de haber algun error, devolvemos un JsonResponse con el error
            # para que sea mostrado por AJAX en el HTML

            if len(error) > 0:
                contexto['error'] = error
                contexto['exitoso'] = False
                return JsonResponse(contexto)

            else:
                lista_semanas = []
                instancia_tipo = NomTipoSemanas.objects.get(tipo = tipo)
                #instancia_tipo = NomTipoSemanas(tipo = instancia_tipo.tipo, nombre=instancia_tipo.nombre)

                # Preparamos los nuevos registros para ser subidos a la base de datos y los
                # mandamos a lista_semanas para ser subidos por bulk_create
                contador = 0
                for fecha in lista_fecha_inicial:
                    par_semanas = NomSemanas(
                        semana = lista_id[contador],
                        fecha_inicial = string_a_datetime(lista_fecha_inicial[contador]),
                        fecha_final = string_a_datetime(lista_fecha_final[contador]),
                        cerrada = False,
                        anio = datetime.today().year,
                        generado = False,
                        tipo_semana = instancia_tipo
                    )

                    lista_semanas.append(par_semanas)
                    contador = contador + 1

                lista_semanas = NomSemanas.objects.bulk_create(lista_semanas)

                # Devolvemos un JsonResponse con la variable exitoso True, para
                # que AJAX redirija al cliente a la lista de tipos de semanas
                contexto['exitoso'] = True
                return JsonResponse(contexto)

        else:
            return render(request, 'nomina/catalogos/semanas/registro_semanas.html', contexto)
    else:
        return redirect('users_app:user_error')


class ListaTiposSemanas(LoginAndActiveMixin, PermisoNomina, View):
    model = NomTipoSemanas
    template_name = 'nomina/catalogos/semanas/lista_semanas.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['lista_tipos_semana'] = self.model.objects.all()
        return contexto

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ConsultarTiposSemanas(LoginAndActiveMixin, PermisoNomina, View):
    model = NomSemanas
    template_name = 'nomina/catalogos/semanas/consulta_semanas.html'
    login_url = reverse_lazy('users_app:user_login')

    def get_context_data(self, *args, **kwargs):
        contexto = {}
        tipo_semana = self.kwargs['pk']
        tipo_semana = NomTipoSemanas.objects.filter(tipo = tipo_semana).values('tipo')[0]['tipo']
        contexto['tipo'] = tipo_semana
        contexto['lista_semanas'] = self.model.objects.filter(tipo_semana = tipo_semana)
        return contexto

    def get(self, request, *args, **kwargs):
        return render (request, self.template_name, self.get_context_data())