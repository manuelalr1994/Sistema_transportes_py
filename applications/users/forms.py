from django import forms
from .models import User
from django.contrib.auth import authenticate

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña',
                'class':'form_control',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir Contraseña',
                'class':'form_control',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'nombres', 'apellidos', 'genero', 'password1', 'password2')
        widgets = {
            'username' : forms.TextInput(
                attrs = {
                    'placeholder':'Usuario',
                    'class':'form_control',
                }
            ),
            'email' : forms.TextInput(
                attrs = {
                    'placeholder':'Email',
                    'class':'form_control',
                }
            ),
            'nombres' : forms.TextInput(
                attrs = {
                    'placeholder':'Nombres',
                    'class':'form_control',
                }
            ),
            'apellidos' : forms.TextInput(
                attrs = {
                    'placeholder':'Apellidos',
                    'class':'form_control',
                }
            ),
            'genero' : forms.Select(
                attrs = {
                    'placeholder':'Sexo',
                    'class':'form_control',
                }
            ),
        }

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')

class LoginForm(forms.Form):

    username = forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={

            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={

            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    class Meta:
        model = User
        fields = ('password1', 'password2')

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Actual',
                'class':'form_control',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Nueva',
                'class':'form_control',
            }
        )
    )