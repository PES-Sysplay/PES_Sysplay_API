from django.contrib.auth import authenticate, login as djangologin, logout as djangologout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from user.emails import send_email_invitation
from user.forms import LoginForm, RegisterForm
from user.mixins import OrganizerAdminPermission
from user.models import Organizer
from user.tables import OrganizerTable


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('root'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = LoginForm(request.POST)
        next_ = request.GET.get('next', '/')
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                Organizer.objects.get(user__username=username)
                user = authenticate(username=username, password=password)
                if user and user.is_active:
                    djangologin(request, user)
                    resp = HttpResponseRedirect(next_)
                    return resp
                else:
                    form.add_error(None, 'Usuario o contraseña incorrecta.')
                    form.add_error('password', '')
                    form.add_error('username', '')

            except Organizer.DoesNotExist:
                form.add_error(None, 'No eres un organizador.')
                form.add_error('password', '')
                form.add_error('username', '')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    djangologout(request)
    return HttpResponseRedirect(reverse('login'))


class OrganizerListView(OrganizerAdminPermission, SingleTableView):
    template_name = 'organizer_list.html'
    table_class = OrganizerTable
    model = Organizer

    def get_queryset(self):
        organizer_admin = get_object_or_404(Organizer, user=self.request.user)
        return Organizer.objects.filter(organization=organizer_admin.organization)


class InviteOrganizerView(OrganizerAdminPermission, TemplateView):
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RegisterForm()
        context.update({
            'form': form
        })
        return context

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            invited = form.create_user(request.user)
            send_email_invitation(sender=request.user, invited=invited, password=password,
                                  url=request.build_absolute_uri(reverse('login')))
            return redirect(reverse('manage'))
        context = self.get_context_data()
        context.update({'form': form})
        return render(request=request, template_name=self.template_name, context=context)


class DeleteUserView(OrganizerAdminPermission, View):
    def get(self, request, id):
        if self.has_permission():
            User.objects.get(pk=id).delete()
            return redirect(reverse('manage'))
        raise PermissionDenied()
