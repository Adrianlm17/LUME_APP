from django import forms
from django.contrib.auth.models import User
from .models import Acta, Anuncio, Chat, Comunidad, Empresa, Evento, ExtendsChat, ExtendsGroupChat, Gasto, GroupChat, Incidencia, Motivo, Nota, PagosUsuario, Recibo, SeguroComunidad, UserProfile, Vivienda



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


class UpdateIMGForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['IMG_profile']


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'descripcion']


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["titulo", "IMG_profile"]


class GroupChatForm(forms.Form):
    title = forms.CharField(label='Título', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del grupo'}))
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple'}))
    
    class Meta:
        model = GroupChat
        fields = ["title", "users", "IMG_profile"]


class ExtendsChatForm(forms.ModelForm):
    class Meta:
        model = ExtendsChat
        fields = ["text"]
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'custom-textarea',
                'placeholder': 'Escribe un mensaje...'
            }),
        }



class ExtendsGroupChatForm(forms.ModelForm):
    class Meta:
        model = ExtendsGroupChat
        fields = ["text"]
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'custom-textarea',
                'placeholder': 'Escribe un mensaje...'
            }),
        }

    
class ActaForm(forms.ModelForm):
    class Meta:
        model = Acta
        fields = ['titulo', 'texto', 'archivo']



class GastoForm(forms.ModelForm):
    cantidad_pagada = forms.DecimalField(label='Cantidad pagada', required=False)

    def __init__(self, *args, **kwargs):
        usuarios_comunidad = kwargs.pop('usuarios_comunidad', None)
        super(GastoForm, self).__init__(*args, **kwargs)
        if (usuarios_comunidad):
            self.fields['usuario'].queryset = usuarios_comunidad
            self.fields['usuario'].label_from_instance = lambda obj: obj.email

    class Meta:
        model = Gasto
        fields = ['titulo', 'descripcion', 'cantidad_total', 'cantidad_pagada', 'fecha', 'fecha_tope', 'usuario', 'archivo']
        widgets = {
            'fecha_tope': forms.DateInput(attrs={'type': 'date'}),
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }

class MotivoReciboForm(forms.ModelForm):
    class Meta:
        model = Motivo
        fields = ['tipo', 'cantidad']

MotivoReciboFormSet = forms.inlineformset_factory(
    Recibo, Motivo, form=MotivoReciboForm, extra=1
)

class ReciboForm(forms.ModelForm):
    cantidad_pagada = forms.DecimalField(label='Cantidad pagada', required=False)

    class Meta:
        model = Recibo
        fields = ['titulo', 'descripcion', 'cantidad_total', 'cantidad_pagada', 'fecha', 'fecha_tope', 'archivo']
        widgets = {
            'fecha_tope': forms.DateInput(attrs={'type': 'date'}),
            'fecha': forms.DateInput(attrs={'type': 'date'})
        }

class PagosUsuarioForm(forms.ModelForm):
    class Meta:
        model = PagosUsuario
        fields = ['titulo', 'descripcion', 'fecha', 'cantidad', 'estado', 'archivo', 'cantidad_pagada']


class EditarComunidadForm(forms.ModelForm):

    class Meta:
        model = Comunidad
        fields = ['nombre', 'pais', 'provincia', 'municipio', 'dirrecion', 'portal', 'dinero', 'numero_cuenta']


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ['metodo_pago']


class PorcentajePagoForm(forms.ModelForm):
    class Meta:
        model = Vivienda
        fields = ['porcentaje_pago']


class CrearAnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'descripcion', 'fecha_anuncio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
            'fecha_anuncio': forms.DateInput(attrs={'type': 'date'}),
        }
        

class AsignarUsuarioComunidadForm(forms.ModelForm):
    USER_ROL_CHOICES = [
        ('community_president', 'Community President'),
        ('community_vicepresident', 'Community Vice President'),
        ('community_user', 'Community User'),
    ]

    rol_comunidad = forms.ChoiceField(
        choices=USER_ROL_CHOICES,
        required=False,
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.all()
        self.fields['usuario'].label_from_instance = self.label_from_user_instance
    
    def label_from_user_instance(self, obj):
        return obj.email

    class Meta:
        model = Vivienda
        fields = ['usuario', 'rol_comunidad', 'piso', 'puerta']

class SeguroComunidadForm(forms.ModelForm):
    class Meta:
        model = SeguroComunidad
        fields = ['empresa', 'cubre', 'cantidad', 'pagado', 'fecha_pago', 'fecha_vencimiento']
        labels = {
            'cubre': 'Tipo de cobertura',
            'cantidad': 'Cantidad',
            'pagado': '¿Pagado?',
            'fecha_pago': 'Fecha de pago',
            'fecha_vencimiento': 'Fecha de vencimiento'
        }
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'archivo', 'prioridad']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
        }


class IncidenciaAdminForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('Pendiente de aceptar', 'Pendiente de aceptar'),
        ('Denegada', 'Denegada'),
        ('Aceptada', 'Aceptada'),
        ('Asignada', 'Asignada'),
        ('Finalizada', 'Finalizada'),
    ]

    estado = forms.ChoiceField(choices=ESTADO_CHOICES, required=False)
    
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'archivo', 'prioridad', 'estado', 'empresa', 'gasto', 'valoracion']
        widgets = {
            'valoracion': forms.NumberInput(attrs={'class': 'valoracion', 'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget = forms.Textarea(attrs={'rows': 5})


class IncidenciaEmpresaForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('Aceptada', 'Aceptada'),
        ('Cancelada', 'Cancelada'),
        ('Trabajando', 'Trabajando'),
        ('Terminada', 'Terminada'),
    ]

    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        )
    
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'estado', 'gasto', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget = forms.Textarea(attrs={'rows': 5})


class EditarEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion', 'telefono', 'correo', 'pais', 'provincia', 'municipio', 'direccion', 'tags']


class UpdateIMGEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['IMG_profile']


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['title', 'descripcion', 'date', 'max_attendees', 'image', 'visibility', 'comunidad', 'direccion']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EventoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['comunidad'].queryset = Comunidad.objects.filter(vivienda__usuario=user).distinct()


