from django import forms

from applications.fletes.catalogos.camiones.models import Camiones

class FormularioCamiones(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = Camiones

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('codigo', 'nombre', 'alias', 'compania_fletera', 'costo_hra')

        # Se definen los atributos de los campos HTML
        widgets = {
            'codigo' : forms.TextInput(
                attrs = {
                    'placeholder':'Codigo',
                    'class':'form_control',
                }
            ),
            'nombre' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombre',
                    'class':'form_control',
                }
            ),
            'alias' : forms.TextInput(
                attrs = {
                    'placeholder':'Alias',
                    'class':'form_control',
                }
            ),
            'costo_hra' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                }
            ),
            'compania_fletera' : forms.Select(
                attrs = {
                    'class':'form_control',
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[key] = valor.upper()

        return cleaned_data