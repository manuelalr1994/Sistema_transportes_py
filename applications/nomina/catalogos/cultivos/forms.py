from django import forms
from applications.nomina.catalogos.cultivos.models import Cultivos, Variedad


class FormularioCultivo(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = Cultivos

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('codigo','nombre')

        # Se definen los atributos de los campos HTML
        widgets = {
            'codigo' : forms.TextInput(
                attrs = {
                    'id':'cultivo',
                    'required' : 'True',
                    'class' : 'form_control'

                }
            ),
            'nombre' : forms.TextInput(
                attrs = {
                    'id':'nombre_cultivo',
                    'disabled':'True',
                    'required' : 'True',
                    'class' : 'form_control'

                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[key] = valor.upper()

        return cleaned_data



class FormularioVariedad(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = Variedad

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('codigo','nombre')

        # Se definen los atributos de los campos HTML
        widgets = {
            'codigo' : forms.TextInput(
                attrs = {
                    'id':'variedad',
                    'disabled':'True',
                    'required' : 'True',
                    'class' : 'form_control'

                }
            ),
            'nombre' : forms.TextInput(
                attrs = {
                    'id':'nombre_variedad',
                    'disabled':'True',
                    'required' : 'True',
                    'class' : 'form_control'

                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[key] = valor.upper()

        return cleaned_data