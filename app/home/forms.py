from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)



class UserProfileEditForm(forms.ModelForm):
    LANG_CHOICES = [
        ('es', 'Español'),
        ('cat', 'Català'),
        ('en', 'English'),
        ('de', 'Deutsch'),
    ]
    phone = forms.RegexField(regex=r'^\d{9}$', error_messages={'invalid': 'Introduce un número de teléfono válido.'})
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    lang = forms.ChoiceField(choices=LANG_CHOICES)
    # IMG_profile = forms.FileField(required=False)

    class Meta:
        model = UserProfile
        fields = ['phone', 'birthday', 'lang', 'IMG_profile']
