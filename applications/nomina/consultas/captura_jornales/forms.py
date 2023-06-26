from django import forms

from applications.nomina.consultas.captura_jornales.models import NomJornales

class FormularioJornales(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = NomJornales

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('campo_agricola', 'tipo_semana', 'semana', 'cuadrillero', 'fecha', 'referencia',
        'temporada', 'labor', 'empleado', 'total_dinero', 'total_hrs_extra', 'total_dinero_hrs_extra')


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
            'temporada' : forms.Select(
                choices = (('V','Verano'),('I','Invierno')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'referencia' : forms.TextInput(
                attrs = {
                    'class':'form_control',
                }
            ),
            'labor' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'labor',

                }
            ),
            'empleado' : forms.Select(
                attrs = {
                    'class':'form_control',
                    'id':'empleado',

                }
            ),
            'total_dinero' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                    'id':'total_dinero',

                }
            ),
            'total_hrs_extra' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                    'id':'total_hrs_extra',

                }
            ),
        }

