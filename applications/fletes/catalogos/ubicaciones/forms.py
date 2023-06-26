from django import forms

from applications.nomina.catalogos.ubicaciones.models import ubicaciones

class FormularioUbicaciones(forms.ModelForm):
    
    class Meta:

        model = ubicaciones

        fields = ('nombre', 'codigo')

        widgets = {
            'nombre' : forms.TextInput(
                attrs = {
                    'placeholder' : 'Ubicación',
                    'class' : 'form_control',
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[key] = valor.upper()

        return cleaned_data

    def clean_nombre(self, *args, **kwargs):
        nombre = self.cleaned_data.get("nombre")
        if ubicaciones.objects.filter(nombre__iexact = nombre).exists():
            raise forms.ValidationError("Ese nombre de ubicacion ya existe")
        return nombre