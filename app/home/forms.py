from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['phone', 'birthday', 'country', 'city', 'address', 'floor', 'door', 'img_profile', 'lang']

#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         self.fields['phone'].widget.attrs.update({'class': 'form-control'})
#         self.fields['birthday'].widget.attrs.update({'class': 'form-control'})
#         self.fields['country'].widget.attrs.update({'class': 'form-control'})
#         self.fields['city'].widget.attrs.update({'class': 'form-control'})
#         self.fields['address'].widget.attrs.update({'class': 'form-control'})
#         self.fields['floor'].widget.attrs.update({'class': 'form-control'})
#         self.fields['door'].widget.attrs.update({'class': 'form-control'})
#         self.fields['img_profile'].widget.attrs.update({'class': 'form-control'})
#         self.fields['lang'].widget.attrs.update({'class': 'form-control'})

#         user_fields = ['username', 'first_name', 'last_name', 'email']
#         for field in user_fields:
#             initial_value = getattr(self.instance, field)
#             self.fields[field] = forms.CharField(
#                 label=User._meta.get_field(field).verbose_name.capitalize(),
#                 initial=initial_value,
#                 widget=forms.TextInput(attrs={'class': 'form-control'}),
#                 required=False
#             )


#     def save(self, commit=True):
#         profile = super(UserProfileForm, self).save(commit=False)
            
#         user = profile
#         user.username = self.cleaned_data['username']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
        
#         if commit:    
#             user.save()
#             profile.save()
        
#         return profile
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)

    

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'birthday', 'country', 'city', 'address', 'floor', 'door', 'img_profile', 'lang']

    phone = forms.CharField(max_length=20, required=False)
    birthday = forms.DateField(required=False)
    country = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=100, required=False)
    floor = forms.CharField(max_length=100, required=False)
    door = forms.CharField(max_length=100, required=False)
    img_profile = forms.ImageField(required=False)
    lang = forms.CharField(max_length=10, required=False)