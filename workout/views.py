from django.shortcuts import redirect
from django.urls import reverse


def home(request):
    if request.user.organizer.admin:
        name = 'manage'
    else:
        name = 'activity_list_view'
    return redirect(reverse(name))
