from django.shortcuts import render, redirect
from .forms import FormularioCierreSemana
from django.http import JsonResponse, QueryDict
from applications.fletes.procesos.capturas_fleteras.models import FleJornada
from applications.facturacion.procesos.procesar_maquila.models import FletesMaquilas
from applications.facturacion.procesos.procesar_maquila.forms import FormularioFletesMaquilas

# Create your views here.

def cerrarSemana(request):
    if request.user.permisos_fletes:
        context = {}
        html_template = "fletes/utilerias/cierre_semana.html"

        # Como el submit va a ser gestionado por AJAX, solo vamos a mandar el formulario cuando se solicita un GET
        # para el POST lo gestionara AJAX, por ende no ocupamos volver a renderizar el formulario 
        if request.method == "GET":
            context["form"] = FormularioCierreSemana()

        if request.method == "POST":
            # Cerramos la Semana
            instancia_cierre = FormularioCierreSemana(request.POST)

            if instancia_cierre.is_valid():
                cierre_data = instancia_cierre.cleaned_data
                capturas_cierre = FleJornada.objects.filter(campo_agricola=cierre_data['campo_agricola'], semana=cierre_data['semana'], tipo_semana=cierre_data['tipo_semana'])

                if not len(capturas_cierre) > 0:
                    context['mensaje_exito'] = "No hay capturas para esta semana, por lo que no se puede cerrar"
                    return JsonResponse(context)

                for captura in capturas_cierre:
                    captura.cerrada = True

                FleJornada.objects.bulk_update(capturas_cierre, ['cerrada'])

                # ----------- Generamos la maquila referente a la semana cerrada ------------

                # Calculamos la cantidad de carros y de horas de fletes
                cant_carros = len(FleJornada.objects.filter(campo_agricola=cierre_data['campo_agricola'], semana=cierre_data['semana'], tipo_semana=cierre_data['tipo_semana']).values_list('camion', flat=True).distinct())
                lista_capturas_maquila = FleJornada.objects.filter(campo_agricola=cierre_data['campo_agricola'], semana=cierre_data['semana'], tipo_semana=cierre_data['tipo_semana'])
                hrs_fletes = 0

                for captura in lista_capturas_maquila:
                    hrs_fletes = hrs_fletes + captura.total_hrs

                # Creamos la instancia del formulario con un querydict mutable
                maquila_dict = {'campo_agricola':cierre_data['campo_agricola'], 'semana':cierre_data['semana'], 
                                'tipo_semana':cierre_data['tipo_semana'], 'cant_carros':cant_carros, 'hrs_fletes':hrs_fletes}
                maquila_querydict = QueryDict('', mutable=True)
                maquila_querydict.update(maquila_dict)
                formulario_maquila = FormularioFletesMaquilas(maquila_querydict)

                if formulario_maquila.is_valid():
                    formulario_maquila.save()

                # Devolvemos mensaje de exito al frontend
                context['mensaje_exito'] = "La semana ha sido cerrada con exito"
                return JsonResponse(context)

            context['mensaje_exito'] = "Introduzca un formulario valido, por favor"
            return JsonResponse(context)

        return render(request, html_template, context)
    else:
        return redirect('users_app:user_error')
