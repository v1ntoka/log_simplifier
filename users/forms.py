from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class MyAuthForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, 'placeholder': 'Логин', 'class': 'form-control'}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", 'placeholder': 'Пароль', 'class': 'form-control'}),
    )
