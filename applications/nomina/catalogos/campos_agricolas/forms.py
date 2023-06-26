from django import forms

from applications.nomina.catalogos.campos_agricolas.models import NomCampos

class FormularioCampos(forms.ModelForm):

    class Meta:

        model = NomCampos

        fields = ('nombre', 'descuento_sindical', 'tipos_semana', 'costo_hra_extra')

        widgets = {
            'nombre' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Nombre',
                    'class':'form_control',
                }
            ),
            'costo_hra_extra' : forms.NumberInput(
                attrs = {
                    'placeholder' : 'Costo Hora Extra',
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