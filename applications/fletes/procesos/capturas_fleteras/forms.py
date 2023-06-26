from django import forms

from applications.fletes.procesos.capturas_fleteras.models import FleJornada

class FormularioJornada(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = FleJornada

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('campo_agricola', 'tipo_semana', 'semana', 'cuadrillero', 'cultivo',
        'variedad', 'labor', 'camion', 'fecha', 'hora_entrada','hora_salida',
        'costo_hra','total_hrs','importe')


        # Se definen los atributos de los campos HTML
        widgets = {
            'campo_agricola' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'campo_agricola',
                }
            ),
            'tipo_semana' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'tipo_semana',
                }
            ),
            'semana' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'semana',

                }
            ),
            'cuadrillero' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'cuadrillero',

                }
            ),
            'cultivo' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'cultivo',
                }
            ),
            'variedad' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'variedad',
                }
            ),
            'labor' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'labor',
                }
            ),
            'camion' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'camion',
                }
            ),
            'fecha' : forms.DateInput(
                attrs = {
                    'id':'fecha',
                }
            ),
            'hora_entrada' : forms.NumberInput(
                attrs = {
                    'id':'hora_entrada',
                },
            ),
            'hora_salida' : forms.NumberInput(
                attrs = {
                    'id':'hora_salida',
                },
            ),
            'costo_hra' : forms.NumberInput(
                attrs = {
                    'id':'costo_hra',
                },
            ),
            'total_hrs' : forms.NumberInput(
                attrs = {
                    'id':'total_hrs',
                },
            ),
            'importe' : forms.NumberInput(
                attrs = {
                    'id':'importe',
                },
            ),
        }

