from django import forms
from django.contrib.auth.models import User

from user.models import Organizer


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Usuario')
    password = forms.CharField(required=True, label='Contraseña', widget=forms.PasswordInput)


class RegisterForm(LoginForm):
    password2 = forms.CharField(required=True, label='Confirme la contraseña', widget=forms.PasswordInput)
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput)
    name = forms.CharField(required=True, label='Nombre', max_length=150)
    admin = forms.BooleanField(label='Administrador', required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            self.add_error('password', 'Las contraseñas no coinciden.')
            self.add_error('password2', '')
            self.add_error(None, 'Las contraseñas no coinciden.')
        return cleaned_data

    def create_user(self, request_user):
        user = User(
            email=self.cleaned_data.get('email'),
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('name'),
        )
        user.set_password(self.cleaned_data.get('password'))
        organization = Organizer.objects.get(user=request_user).organization
        user.save()
        organizer = Organizer(
            user=user,
            admin=self.cleaned_data.get('admin'),
            organization=organization,
        )
        organizer.save()
        return organizer
