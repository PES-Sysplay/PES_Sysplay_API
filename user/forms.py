from django import forms
from django.contrib.auth.models import User

from user.models import Organizer, Organization


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


class ImageForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'onchange': 'submit()', 'hidden': True})
        }


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(required=True, widget=forms.PasswordInput())
    password_new = forms.CharField(required=True, widget=forms.PasswordInput())
    password_new2 = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password_new', '')
        password2 = cleaned_data.get('password_new2', '')
        if not password1 or not password2 or password2 != password1:
            self.add_error('password_new', '')
            self.add_error('password_new2', '')
            self.add_error(None, 'Las contraseñas no coinciden.')
        return cleaned_data

