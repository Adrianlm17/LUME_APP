from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        ))
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombre",
                "class": "form-control"
            }
        ))

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apellido",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo electrónico",
                "class": "form-control"
            }
        ))

    phone = forms.RegexField(
        regex="^[0-9]{3}-?[0-9]{2}-?[0-9]{3}$",
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "pattern": "[0-9]+",
                "id": "phone",
                "placeholder": "Número de teléfono",
                "class": "form-control"
            }
        )
    )

    country = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "País",
                "class": "form-control"
            }
        ))

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Dirección",
                "class": "form-control"
            }
        ))

    street = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Calle",
                "class": "form-control"
            }
        ))

    number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Número",
                "class": "form-control"
            }
        ))

    floor = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Piso",
                "class": "form-control"
            }
        ))

    door = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Puerta",
                "class": "form-control"
            }
        ))

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "class": "form-control"
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar contraseña",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'phone', 'country', 'address', 'street', 'number', 'floor', 'door', 'password1', 'password2')
