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
        return redirect(reverse('activity_detail'))


class ActivityEdit(ActivityCreate):

    def get_model_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk', default='')
        activity = get_object_or_404(Activity, pk=pk)
        if activity.org != self.request.user.org:
            raise PermissionDenied()
        return activity



