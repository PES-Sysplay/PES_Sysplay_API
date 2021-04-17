from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Usuario')
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput)
