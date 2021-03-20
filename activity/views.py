from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from activity.form import ActivityForm
from activity.models import Activity
from workout.abstract_views import FormView


class CreateActivityView(TemplateView):
    template_name = 'create_activity.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ActivityCreate(FormView):
    template_name = 'create_activity.html'
    form_class = ActivityForm

    def get_success_redirect(self, model_object):
        return redirect(reverse('view_activity', args=[model_object.pk]))


class ActivityView(ActivityCreate):
    template_name = 'create_activity.html'
    form_class = ActivityForm

    def set_form(self, form):
        form.set_read_only()

    def get_model_object(self):
        m_id = self.kwargs.get("id")
        activity = get_object_or_404(Activity, pk=m_id)
        return activity


class ActivityEdit(ActivityCreate):

    def get_model_object(self, *args, **kwargs):
        m_id = self.kwargs.get('id')
        activity = get_object_or_404(Activity, pk=m_id)
        #if activity.org != self.request.user.org:
        #    raise PermissionDenied()
        return activity
