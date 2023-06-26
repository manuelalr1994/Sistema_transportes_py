from django import forms

from applications.fletes.catalogos.compania_fletera.models import CompaniasFleteras

class FormularioCompania(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = CompaniasFleteras

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('codigo', 'cuenta', 'nombre', 'direccion', 
        'ciudad', 'codigo_postal', 'telefono', 'tarjeta', 'rfc', 'colonia', 'estado')

        ESTADO_OPCIONES = (
            ("AGUASCALIENTES", "AGUASCALIENTES"),
            ("BAJA CALIFORNIA", "BAJA CALIFORNIA"),
            ("BAJA CALIFORNIA SUR", "BAJA CALIFORNIA SUR"),
            ("CAMPECHE", "CAMPECHE"),
            ("COAHUILA DE ZARAGOZA", "COAHUILA DE ZARAGOZA"),
            ("COLIMA", "COLIMA"),
            ("CHIAPAS", "CHIAPAS"),
            ("CHIHUAHUA", "CHIHUAHUA"),
            ("CIUDAD DE MÉXICO", "CIUDAD DE MÉXICO"),
            ("DURANGO", "DURANGO"),
            ("GUANAJUATO", "GUANAJUATO"),
            ("GUERRERO", "GUERRERO"),
            ("HIDALGO", "HIDALGO"),
            ("JALISCO", "JALISCO"),
            ("MÉXICO", "MÉXICO"),
            ("MICHOACÁN DE OCAMPO", "MICHOACÁN DE OCAMPO"),
            ("MORELOS", "MORELOS"),
            ("NAYARIT", "NAYARIT"),
            ("NUEVO LEÓN", "NUEVO LEÓN"),
            ("OAXACA", "OAXACA"),
            ("PUEBLA", "PUEBLA"),
            ("QUERÉTARO", "QUERÉTARO"),
            ("QUINTANA ROO", "QUINTANA ROO"),
            ("SAN LUIS POTOSÍ", "SAN LUIS POTOSÍ"),
            ("SINALOA", "SINALOA"),
            ("SONORA", "SONORA"),
            ("TABASCO", "TABASCO"),
            ("TAMAULIPAS", "TAMAULIPAS"),
            ("TLAXCALA", "TLAXCALA"),
            ("VERACRUZ DE IGNACIO DE LA LLAVE", "VERACRUZ DE IGNACIO DE LA LLAVE"),
            ("YUCATÁN", "YUCATÁN"),
            ("ZACATECAS", "ZACATECAS"),
            ("EXTRANJERO", "EXTRANJERO"),
        )

        # Se definen los atributos de los campos HTML
        widgets = {
            'cuenta' : forms.TextInput(
                attrs = {
                    'placeholder':'Cuenta',
                    'class':'form_control'
                }
            ),
            'codigo' : forms.TextInput(
                attrs = {
                    'placeholder':'Codigo',
                    'class':'form_control'
                }
            ),
            'nombre' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombre',
                    'class':'form_control'
                }
            ),
            'direccion' : forms.TextInput(
                attrs = {
                    'placeholder':'Dirección',
                    'class':'form_control'
                }
            ),
            'ciudad' : forms.TextInput(
                attrs = {
                    'placeholder':'Ciudad',
                    'class':'form_control'
                }
            ),
            'codigo_postal' : forms.TextInput(
                attrs = {
                    'placeholder':'Codigo Postal',
                    'class':'form_control'
                }
            ),
            'telefono' : forms.TextInput(
                attrs = {
                    'placeholder':'6621458990',
                    'type' : 'tel',
                    'pattern' : '[0-9]{10}',
                    'class':'form_control'
                }
            ),
            'tarjeta' : forms.TextInput(
                attrs = {
                    'placeholder':'Tarjeta',
                    'class':'form_control'
                }
            ),
            'rfc' : forms.TextInput(
                attrs = {
                    'placeholder':'RFC',
                    'class':'form_control'
                }
            ),
            'colonia' : forms.TextInput(
                attrs = {
                    'placeholder':'Colonia',
                    'class':'form_control'
                }
            ),
            'estado' : forms.Select(
                attrs = {
                    'class':'form_control'
                },
                choices = ESTADO_OPCIONES
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        for key, valor in cleaned_data.items():
            if isinstance(valor, str):
                cleaned_data[key] = valor.upper()

        return cleaned_data
