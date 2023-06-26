
from django import forms

from .models import FletesMaquilas

class FormularioFletesMaquilas(forms.ModelForm):

    class Meta:

        model = FletesMaquilas

        fields = ('campo_agricola', 'semana', 'tipo_semana', 'cant_carros', 'hrs_fletes', 
                'costo_maquila', 'importe_maquila', 'procesada')

        widgets = {
            'campo_agricola' : forms.Select(
                attrs = {
                    'class':'form_control',
                }
            ),
            'semana' : forms.Select(
                attrs = {
                    'class':'form_control',
                }
            ),
            'tipo_semana' : forms.Select(
                attrs = {
                    'class':'form_control',
                }
            ),
            'cant_carros' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                    'step' : '1',
                }
            ),
            'hrs_fletes' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                }
            ),
            'costo_maquila' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                }
            ),
            'importe_maquila' : forms.NumberInput(
                attrs = {
                    'class':'form_control',
                }
            ),
        }