from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django_tables2 import SingleTableView

from activity_action.models import ActivityJoined
from activity_action.tables import CheckinTable
from user.mixins import OrganizerActivityPermission


class CheckinView(OrganizerActivityPermission, SingleTableView):
    table_class = CheckinTable
    template_name = 'checkin.html'
    model = ActivityJoined

    def get_queryset(self):
        queryset = super().get_queryset()
        m_id = self.kwargs.get("id")
        queryset = queryset.filter(activity_id=m_id)
        return queryset

    def post(self, request, id):
        token = request.POST.get('token', '')
        if not token:
            messages.error(request, 'Error del código qr o el qr esta vacio', extra_tags='danger')
        else:
            try:
                activity = ActivityJoined.objects.get(token=token, activity_id=id)
                if activity.checked_in:
                    messages.error(request, 'El cliente ya ha hecho el check-in', extra_tags='danger')
                else:
                    activity.checked_in = True
                    activity.save()
                    messages.success(request, 'Cliente registrado con éxito')
            except (ActivityJoined.DoesNotExist, ValidationError):
                messages.error(request, 'Client no encontrado', extra_tags='danger')
        return redirect(reverse('checkin-list', args=[id]))
