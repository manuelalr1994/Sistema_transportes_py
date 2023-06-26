from django import forms
from .models import NomPuestos

class FormularioPuestos(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = NomPuestos

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('nombre',)

        # Se definen los atributos de los campos HTML
        widgets = {
            'codigo' : forms.TextInput(
                attrs = {
                    'class':'form_control',
                }
            ),
            'nombre' : forms.TextInput(
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

    def clean_nombre(self, *args, **kwargs):
        nombre = self.cleaned_data.get("nombre")
        if NomPuestos.objects.filter(nombre__iexact = nombre).exists():
            raise forms.ValidationError("Ese nombre de puesto ya existe")
        return nombre