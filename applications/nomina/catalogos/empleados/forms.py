from django import forms
from .models import NomEmpleado
import datetime

class FormularioEmpleados(forms.ModelForm):
    
    class Meta:

        # Se define el modelo para este formulario
        model = NomEmpleado

        # Se definen los campos que se van a utilizar en Modelos
        fields = ('codigo','fecha_alta','tipo_contrato','num_tarjeta','cuenta_banco','paterno','materno','nombres','fecha_nacimiento','tipo_periodo','salario_base','base_cotizacion','puesto','integrado','comida','campo_agricola','estatus','cuadrillero','num_seguro_social','num_infonavit','rfc_trabajador','curp','sexo','edo_civil','nombre_madre','nombre_padre','domicilio','codigo_postal','lugar_nacimiento','familiar_referencia_1','telefono_referencia_1','familiar_referencia_2','telefono_referencia_2')

        # Se definen los atributos de los campos HTML
        widgets = {
            'codigo' : forms.TextInput(
                attrs = {
                    'class':'form_control',
                }
            ),
            'fecha_alta' : forms.DateInput(
                attrs = {
                    'class':'form_control',
                    'type':'date'
                }
            ),
            'tipo_contrato' : forms.Select(
                choices = (('F','fijo'),('T','temporal')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'num_tarjeta' : forms.TextInput(
                attrs = {
                    'placeholder':'Numero de tarjeta',
                    'class':'form_control',
                }
            ),
            'cuenta_banco' : forms.TextInput(
                attrs = {
                    'placeholder':'Cuenta de banco',
                    'class':'form_control',
                }
            ),
            'paterno' : forms.TextInput(
                attrs = {
                    'placeholder':'Apellido paterno',
                    'class':'form_control',
                }
            ),
            'materno' : forms.TextInput(
                attrs = {
                    'placeholder':'Apellido materno',
                    'class':'form_control',
                }
            ),
            'nombres' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombres',
                    'class':'form_control',
                }
            ),
            'fecha_nacimiento' : forms.DateInput(
                attrs = {
                    'class':'form_control',
                    'type':'date',
                }
            ),
            'tipo_periodo' : forms.Select(
                choices = (('O','otro'),('I','indefinido')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'salario_base' : forms.TextInput(
                attrs = {
                    'placeholder':'Salario base',
                    'class':'form_control',
                }
            ),
            'base_cotizacion' : forms.Select(
                choices = (('S','si'),('N','no')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'puesto' : forms.TextInput(
                attrs = {
                    'placeholder':'Puesto',
                    'class':'form_control',
                }
            ),
            'integrado' : forms.Select(
                choices = (('S','si'),('N','no')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'comida' : forms.Select(
                choices = (('S','si'),('N','no')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'campo_agricola' : forms.Select(
                attrs = {
                    'class':'form_control',
                }
            ),
            'estatus' : forms.Select(
                choices = (('A','activo'),('I','inactivo')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'cuadrillero' : forms.Select(
                attrs = {
                    'class':'form_control',
                }
            ),
            'num_seguro_social' : forms.TextInput(
                attrs = {
                    'placeholder':'Num. Seguro Social',
                    'class':'form_control',
                }
            ),
            'num_infonavit' : forms.TextInput(
                attrs = {
                    'placeholder':'Num. Infonavit',
                    'class':'form_control',
                }
            ),
            'rfc_trabajador' : forms.TextInput(
                attrs = {
                    'placeholder':'RFC',
                    'class':'form_control',
                }
            ),
            'curp' : forms.TextInput(
                attrs = {
                    'placeholder':'CURP',
                    'class':'form_control',
                }
            ),
            'sexo' : forms.Select(
                choices = (('M','masculino'),('F','femenino')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'edo_civil' : forms.Select(
                choices = (('S','soltero'),('C','casado')),
                attrs = {
                    'class':'form_control',
                }
            ),
            'nombre_madre' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombre de la madre',
                    'class':'form_control',
                }
            ),
            'nombre_padre' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombre del padre',
                    'class':'form_control',
                }
            ),
            'domicilio' : forms.TextInput(
                attrs = {
                    'placeholder':'Domicilio',
                    'class':'form_control',
                }
            ),
            'codigo_postal' : forms.TextInput(
                attrs = {
                    'placeholder':'Codigo Postal',
                    'class':'form_control',
                }
            ),
            'lugar_nacimiento' : forms.TextInput(
                attrs = {
                    'placeholder':'Lugar de nacimiento',
                    'class':'form_control',
                }
            ),
            'familiar_referencia_1' : forms.TextInput(
                attrs = {
                    'placeholder':'Familiar de referencia',
                    'class':'form_control',
                }
            ),
            'telefono_referencia_1' : forms.TextInput(
                attrs = {
                    'placeholder':'Telefono de referencia',
                    'class':'form_control',
                }
            ),
            'familiar_referencia_2' : forms.TextInput(
                attrs = {
                    'placeholder':'Familiar de referencia 2',
                    'class':'form_control',
                }
            ),
            'telefono_referencia_2' : forms.TextInput(
                attrs = {
                    'placeholder':'Telefono de referencia 2',
                    'class':'form_control',
                }
            ),
        }