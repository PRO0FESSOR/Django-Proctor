from django import forms 
from django.contrib.auth.forms import AuthenticationForm , UsernameField
from django.utils.translation import gettext , gettext_lazy as _

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control','autofocus': True}))
    password = forms.CharField(label=_("password"), strip = False ,widget=forms.PasswordInput(attrs={'autocomplete' : 'current-password','class':'form-control'}))


