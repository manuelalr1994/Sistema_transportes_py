from django import forms
from applications.nomina.catalogos.labores.models import NomLabores

class FormularioLabores(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = NomLabores

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('nombre',)

        # Se definen los atributos de los campos HTML
        widgets = {
            'nombre' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombre',
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
        if NomLabores.objects.filter(nombre__iexact = nombre).exists():
            raise forms.ValidationError("Ese nombre de labor ya existe")
        return nombre
