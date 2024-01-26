# en tu_app/forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from .models import Usuario  # Asegúrate de importar tu modelo de usuario

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
    )
