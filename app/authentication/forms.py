from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
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
                "placeholder": "Name",
                "class": "form-control"
            }
        ))

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Surname",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Gmail",
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
                "placeholder": "Phone",
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'phone', 'country', 'address', 'street', 'number', 'floor', 'door', 'password1', 'password2')
