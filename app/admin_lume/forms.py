from django import forms
from django.contrib.auth.models import User
from app.home.models import Comunidad, Empresa, Trabajador, UserProfile, Vivienda
from django.contrib.auth.forms import UserCreationForm


class CrearUserProfileForm(forms.ModelForm):
    LANG_CHOICES = [
        ('es', 'Español'),
        ('cat', 'Català'),
        ('en', 'English'),
        ('de', 'Deutsch'),
    ]
    USER_ROL_CHOICES = [
        ('lume', 'LUME WORKER'),
        ('community_user', 'Community User'),
        ('community_worker', 'Comunity Worker'),
        ('company_boss', 'Company Boss'),
        ('company_user', 'Company User'),
    ]
    
    phone = forms.RegexField(
        regex=r'^\d{9}$', 
        error_messages={'invalid': 'Introduce un número de teléfono válido.'},
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Phone",
                "class": "form-control"
            }
        ))
    
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                "placeholder": "Birthday",
                "class": "form-control"
                },
            ), 
        required=False)
    
    lang = forms.ChoiceField(
        choices=LANG_CHOICES, 
        required=False
        )
    
    user_rol = forms.ChoiceField(
        choices=USER_ROL_CHOICES,
        required=False,
        )
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'birthday', 'lang', 'user_rol']
    


class CrearComunidadForm(forms.ModelForm):

    class Meta:
        model = Comunidad
        fields = ['nombre', 'pais', 'provincia', 'municipio', 'calle', 'portal', 'dinero']



class CrearCompanyForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion', 'telefono', 'correo', 'pais', 'provincia', 'municipio', 'direccion']



class CrearViviendaForm(forms.ModelForm):
    
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
        fields = ['usuario', 'comunidad', 'rol_comunidad', 'piso', 'puerta']



class CrearTrabajadorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.all()
        self.fields['usuario'].label_from_instance = self.label_from_user_instance
    
    def label_from_user_instance(self, obj):
        return obj.email

    class Meta:
        model = Trabajador
        fields = ['usuario', 'empresa']
