from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from activity.emails import send_email_activity_changed, send_email_activity_cancelled
from activity.form import ActivityForm
from activity.models import Activity
from user.mixins import OrganizerPermission, OrganizerActivityPermission
from user.models import Organizer
from workout.abstract_views import FormView


class ActivityCreate(OrganizerPermission, FormView):
    template_name = 'create_activity.html'
    form_class = ActivityForm

    def save_model(self, model_object):
        organizer = Organizer.objects.get(user=self.request.user)
        model_object.created_by = organizer
        model_object.organized_by = organizer.organization
        model_object.save()

    def get_success_redirect(self, model_object):
        return redirect(reverse('view_activity', args=[model_object.pk]))


class ActivityView(OrganizerActivityPermission, ActivityCreate):
    template_name = 'create_activity.html'
    form_class = ActivityForm

    def get_context_data(self, model_object=None, **kwargs):
        context = super().get_context_data(model_object, **kwargs)
        model_object = self.get_model_object()
        if model_object:
            reports = set(model_object.activityjoined_set.all().values_list('activityreport__comment', flat=True))
            if None in reports:
                reports.remove(None)
            context.update({'reports': reports})
        return context

    def set_form(self, form):
        form.set_read_only()

    def get_model_object(self):
        m_id = self.kwargs.get("id")
        activity = get_object_or_404(Activity, pk=m_id)
        return activity


class ActivityEdit(OrganizerActivityPermission, ActivityCreate):

    def get_model_object(self, *args, **kwargs):
        m_id = self.kwargs.get('id')
        activity = get_object_or_404(Activity, pk=m_id)
        return activity

    def save_model(self, model_object):
        old_object = self.get_model_object()
        super().save_model(model_object)
        send_email_activity_changed(old=old_object, new=model_object)


class ActivityListView(OrganizerPermission, TemplateView):
    template_name = 'my_activities.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organizer = get_object_or_404(Organizer, user=self.request.user)
        activities = Activity.objects.filter(organized_by=organizer.organization).order_by('-start_date')
        context.update({'activities': activities})
        return context


class ActivityCancelView(OrganizerActivityPermission, View):
    def get(self, request, id):
        activity = get_object_or_404(Activity, pk=id)
        activity.status = Activity.STATUS_CANCELLED
        activity.save()
        send_email_activity_cancelled(activity)
        messages.success(request, 'Actividad cancelada')
        return redirect(reverse('view_activity', args=[id]))
