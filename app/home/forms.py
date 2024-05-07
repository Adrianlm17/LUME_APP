from django import forms
from django.contrib.auth.models import User
from .models import Acta, Chat, Comunidad, ExtendsChat, Gasto, Motivo, Nota, Recibo



class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Primer apellido",
                "class": "form-control"
            }
        ))
    
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Segundo apellido",
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'descripcion']


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["titulo"]


class ExtendsChatForm(forms.ModelForm):
    class Meta:
        model = ExtendsChat
        fields = ["text"]



class ActaForm(forms.ModelForm):
    class Meta:
        model = Acta
        fields = ['titulo', 'comunidad', 'texto']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['comunidad'].queryset = Comunidad.objects.filter(
                vivienda__usuario=user,
                vivienda__rol_comunidad__in=['community_president', 'community_vicepresident']
            )
        else:
            self.fields['comunidad'].queryset = Comunidad.objects.none()



class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['titulo', 'descripcion', 'cantidad_total', 'fecha_tope', 'usuario']
        widgets = {'fecha_tope': forms.DateInput(attrs={'type': 'date'})}

class MotivoReciboForm(forms.ModelForm):
    class Meta:
        model = Motivo
        fields = ['tipo', 'cantidad']

MotivoReciboFormSet = forms.inlineformset_factory(
    Recibo, Motivo, form=MotivoReciboForm, extra=1
)

class ReciboForm(forms.ModelForm):
    class Meta:
        model = Recibo
        fields = ['titulo', 'descripcion', 'fecha_tope', 'cantidad_total']
        widgets = {'fecha_tope': forms.DateInput(attrs={'type': 'date'})}