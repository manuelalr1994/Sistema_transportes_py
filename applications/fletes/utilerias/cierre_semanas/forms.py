from django import forms

from applications.fletes.procesos.capturas_fleteras.models import FleJornada

class FormularioCierreSemana(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = FleJornada

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('campo_agricola', 'tipo_semana', 'semana')


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
        }

