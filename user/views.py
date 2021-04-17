from django.contrib.auth import authenticate, login as djangologin, logout as djangologout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.forms import LoginForm
from user.models import Organizer


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
            except Organizer.DoesNotExist:
                form.add_error(None, 'No eres un organizador.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    djangologout(request)
    return HttpResponseRedirect(reverse('login'))
