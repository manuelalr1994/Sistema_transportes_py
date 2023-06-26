from django.shortcuts import render, redirect
from django.http import QueryDict
from urllib import request
from django.urls import reverse_lazy
from .forms import FormularioCultivo, FormularioVariedad
from applications.nomina.catalogos.cultivos.models import Cultivos, Variedad
from django.http import JsonResponse
from applications.users.mixins import LoginAndActiveMixin, PermisoFletes
from django.views.generic import ListView


# Llevar un recuento de los codigos que pudieron ser recuperados con un diccionario booleano
codigos_recuperados = {'cultivo':False, 'variedad':False}

# Create your views here.
def RegistrarCultivo(request):

    template_name = 'fletes/catalogos/cultivos/registro_cultivo.html'
    context = {}
    if request.user.permisos_fletes:
        if request.method == "POST":
            
            data = {}

            for key, value in request.POST.items():
                if len(value) <= 0:
                    data['error'] = 'Todos los campos deben ser llenados'
                    data['exitoso'] = False
                    return JsonResponse(data)

            # 
            cultivo_dict = {'codigo':request.POST.get('codigo_cultivo'), 'nombre':request.POST.get('nombre_cultivo')}
            cultivo_querydict = QueryDict('', mutable=True)
            cultivo_querydict.update(cultivo_dict)

            variedad_dict = {'codigo':request.POST.get('codigo_variedad'), 'nombre':request.POST.get('nombre_variedad')}
            variedad_querydict = QueryDict('', mutable=True)
            variedad_querydict.update(variedad_dict)

            print(variedad_querydict)

            formulario_cultivos = FormularioCultivo(cultivo_querydict)
            formulario_variedades = FormularioVariedad(variedad_querydict)

            print(formulario_cultivos)
            print(formulario_variedades)

            # Corroboramos que los formularios son validos
            if formulario_cultivos.is_valid() and formulario_variedades.is_valid():

                print('entre a formularios validos')

                cultivo = Cultivos(**formulario_cultivos.cleaned_data)
                variedad = Variedad(**formulario_variedades.cleaned_data)

                # Corroboramos que la cadena de codigo es un numero
                if cultivo.codigo.isnumeric() and variedad.codigo.isnumeric():
                    print('entre en son numericos')
                    print(codigos_recuperados['cultivo'])
                    if not codigos_recuperados['cultivo']:
                        print('Codigo no recuperado cultivo, donde codigo es: '+cultivo.codigo)
                        if Cultivos.objects.filter(codigo=cultivo.codigo).exists():
                            print('dentro de cultivo existe')
                            data['error'] = 'El codigo de cultivo ya fue asignado a otro cultivo'
                            data['exitoso'] = False
                            return JsonResponse(data)
                        else:
                            print('dentro de cultivo no existe')
                            cultivo.save()

                    print(codigos_recuperados['variedad'])
                    if not codigos_recuperados['variedad']:
                        id_cultivo = Cultivos.objects.get(codigo = cultivo.codigo).id

                        if Variedad.objects.filter(codigo=variedad.codigo, id_cultivo=id_cultivo).exists():
                            print('dentro variedad existe')
                            data['error'] = 'El codigo de variedad ya fue asignado a otra variedad de este cultivo'
                            data['exitoso'] = False
                            return JsonResponse(data)
                        else:
                            print('dentro variedad no existe')
                            variedad.id_cultivo = Cultivos.objects.get(id = id_cultivo)
                            variedad.save()

                    if all(valor==True for valor in codigos_recuperados.values()):
                        print('entre en todos los valores son true')
                        data['error'] = 'El codigo de variedad ya fue asignado a otra variedad de este cultivo'
                        data['exitoso'] = False
                        return JsonResponse(data)

                    data['exitoso'] = True
                    return JsonResponse(data)

                else:
                    data['error'] = 'Los codigos deben ser numericos'
                    data['exitoso'] = False
                    return JsonResponse(data)
                
            else:
                data['error'] = 'El formulario enviado es invalido'
                data['exitoso'] = False
                return JsonResponse(data)


        else:

            formulario_cultivos = FormularioCultivo()
            formulario_variedades = FormularioVariedad()
            print(formulario_cultivos)
            print(formulario_variedades)
            context['formulario_cultivos'] = formulario_cultivos
            context['formulario_variedades'] = formulario_variedades

            return render(request, template_name, context)
    return redirect('users_app:user_error')
    
# Modulo para mostrar lista de cuadrilleros
class ListaCultivos(LoginAndActiveMixin, PermisoFletes, ListView):
    model = Variedad
    template_name = 'fletes/catalogos/cultivos/lista_cultivos.html'
    login_url = reverse_lazy('users_app:user_login')
    
    # Esta funcion genera el contexto (las variables que entran al Template)
    def get_context_data(self, **kwargs):
        context = {}
        cultivo_buscado = self.request.GET.get('cultivo_buscado')
        if cultivo_buscado is not None:
            context['lista_variedades'] = self.model.objects.filter(id_cultivo__nombre__icontains=cultivo_buscado).order_by('id_cultivo__codigo', 'codigo')
        else:
            context['lista_variedades'] = self.model.objects.all().order_by('id_cultivo__codigo', 'codigo')
        return context

    # Esta funcion define lo que va a pasar cuando se ejecute el metodo GET
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())



# Views for AJAX request
def cargarCultivos(request):

    codigo_cultivo = request.GET.get('codigo_cultivo')
    data = {}

    if codigo_cultivo.isnumeric():

        try:
            cultivo = Cultivos.objects.get(codigo = codigo_cultivo)
            data['nombre_cultivo'] = cultivo.nombre
            data['cultivo_existe'] = True
            data['codigo_cultivo_numerico'] = True
            codigos_recuperados['cultivo'] = True
            return JsonResponse(data)

        except:
            print('entre a cultivo existe false')
            data['cultivo_existe'] = False
            data['codigo_cultivo_numerico'] = True
            codigos_recuperados['cultivo'] = False
            return JsonResponse(data)

    else:
        data['codigo_cultivo_numerico'] = False
        data['error'] = 'El codigo introducido en cultivo no es numerico'
        codigos_recuperados['cultivo'] = False
        return JsonResponse(data)


def cargarVariedades(request):

    codigo_variedad = request.GET.get('codigo_variedad')
    codigo_cultivo = request.GET.get('codigo_cultivo')
    data = {}

    # Corroboramos si el codigo es numerico
    if codigo_variedad.isnumeric():
        # Corroboramos si existe el cultivo, no cargamos variedad si no existe el cultivo
        # ya que no existe, todas las variedades estan vinculadas a un cultivo
        if Cultivos.objects.filter(codigo=codigo_cultivo).exists():
            id_cultivo = Cultivos.objects.get(codigo = codigo_cultivo).id
            # Corroboramos si la variedad existe, si no, no cargamos variedad
            if Variedad.objects.filter(codigo = codigo_variedad, id_cultivo = id_cultivo).exists():
                id_cultivo = Cultivos.objects.get(codigo=codigo_cultivo)
                variedad = Variedad.objects.get(codigo = codigo_variedad, id_cultivo = id_cultivo)
                data['nombre_variedad'] = variedad.nombre
                data['variedad_existe'] = True
                codigos_recuperados['variedad'] = True
                print('Este es el valor actual de variedad en si existe variedad: '+str(codigos_recuperados['variedad']))
                data['codigo_variedad_numerico'] = True
                return JsonResponse(data)
            else:
                print('entre a variedad existe false')
                data['variedad_existe'] = False
                print('Este es el valor actual de variedad en no existe variedad: '+str(codigos_recuperados['variedad']))
                data['codigo_variedad_numerico'] = True
                codigos_recuperados['variedad'] = False
                return JsonResponse(data)
        
        else:
            data['variedad_existe'] = False
            print('Este es el valor actual de variedad en no existe cultivo: '+str(codigos_recuperados['variedad']))
            data['codigo_variedad_numerico'] = True
            codigos_recuperados['variedad'] = False
            return JsonResponse(data)

    else:
        data['codigo_variedad_numerico'] = False
        codigos_recuperados['variedad'] = False
        data['error'] = 'El codigo introducido en variedad no es numerico'
        return JsonResponse(data)

    
