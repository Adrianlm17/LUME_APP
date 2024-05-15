from django import forms
from django.contrib.auth.models import User
from .models import Acta, Anuncio, Chat, Comunidad, Empresa, Evento, ExtendsChat, Gasto, Incidencia, Motivo, Nota, PagosUsuario, Recibo, SeguroComunidad, UserProfile, Vivienda



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
        fields = ["titulo"]


class ExtendsChatForm(forms.ModelForm):
    class Meta:
        model = ExtendsChat
        fields = ["text"]



class ActaForm(forms.ModelForm):
    class Meta:
        model = Acta
        fields = ['titulo', 'texto']



class GastoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        usuarios_comunidad = kwargs.pop('usuarios_comunidad', None)
        super(GastoForm, self).__init__(*args, **kwargs)
        if usuarios_comunidad:
            self.fields['usuario'].queryset = usuarios_comunidad

            # Modificar las etiquetas de los usuarios para mostrar el correo electrónico
            self.fields['usuario'].label_from_instance = lambda obj: obj.email

    class Meta:
        model = Gasto
        fields = ['titulo', 'descripcion', 'cantidad_total', 'fecha', 'fecha_tope', 'usuario']
        widgets = {'fecha_tope': forms.DateInput(attrs={'type': 'date'}), 'fecha': forms.DateInput(attrs={'type': 'date'})}
    

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
        fields = ['titulo', 'descripcion', 'fecha', 'fecha_tope', 'cantidad_total']
        widgets = {'fecha_tope': forms.DateInput(attrs={'type': 'date'}),  'fecha': forms.DateInput(attrs={'type': 'date'})}


class PagosUsuarioForm(forms.ModelForm):
    class Meta:
        model = PagosUsuario
        fields = ['titulo', 'descripcion', 'fecha', 'cantidad', 'estado']


class EditarComunidadForm(forms.ModelForm):

    class Meta:
        model = Comunidad
        fields = ['nombre', 'pais', 'provincia', 'municipio', 'calle', 'portal', 'dinero']


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget = forms.Textarea(attrs={'rows': 5})


class IncidenciaAdminForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['titulo', 'descripcion', 'archivo', 'prioridad', 'estado', 'empresa', 'gasto', 'valoracion', 'fecha_cierre']

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
        fields = ['nombre', 'descripcion', 'telefono', 'correo', 'pais', 'provincia', 'municipio', 'direccion']

class UpdateIMGEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['IMG_profile']


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['title', 'descripcion', 'date', 'max_attendees', 'image', 'visibility', 'comunidad']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EventoForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['comunidad'].queryset = Comunidad.objects.filter(vivienda__usuario=user).distinct()
        

