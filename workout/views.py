from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from user.mixins import OrganizerPermission


class Home(OrganizerPermission, View):
    def get(self, request):
        if request.user.organizer.admin:
            name = 'manage'
        else:
            name = 'activity_list_view'
        return redirect(reverse(name))
