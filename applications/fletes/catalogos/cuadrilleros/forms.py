from django import forms
from applications.nomina.catalogos.cuadrilleros.models import NomCuadrilleros

class FormularioCuadrilleros(forms.ModelForm):

    class Meta:
        model = NomCuadrilleros

        fields = ('nombre', 'campo_agricola')

        widgets = {
            'nombre' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombre',
                    'class':'form_control',
                }
            ),
            'campo_agricola' : forms.Select(
                attrs = {
                    'id':'empresa',
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