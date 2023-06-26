from django import forms

from applications.nomina.catalogos.empresas.models import NomEmpresas
from applications.nomina.catalogos.semanas.models import NomTipoSemanas


class FormularioEmpresas(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = NomEmpresas

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('codigo','nombre','rfc','direccion','colonia','ciudad',
        'estado','cp')

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
            'rfc' : forms.TextInput(
                attrs = {
                    'placeholder':'RFC',
                    'class':'form_control',
                }
            ),
            'direccion' : forms.TextInput(
                attrs = {
                    'placeholder':'Dirección',
                    'class':'form_control',
                }
            ),
            'colonia' : forms.TextInput(
                attrs = {
                    'placeholder':'Colonia',
                    'class':'form_control',
                }
            ),
            'ciudad' : forms.TextInput(
                attrs = {
                    'placeholder':'Municipio',
                    'class':'form_control',
                }
            ),
            'estado' : forms.TextInput(
                attrs = {
                    'placeholder':'Estado',
                    'class':'form_control',
                }
            ),
            'cp' : forms.TextInput(
                attrs = {
                    'placeholder':'Codigo Postal',
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
