from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated

from activity.models import Activity
from user.models import Organizer


class OrganizerPermission(PermissionRequiredMixin):
    def extra(self, organizer):
        return True

    def get_login_url(self):
        return reverse('login')

    def has_permission(self):
        if not self.request.user.is_authenticated:
            return False
        try:
            organizer = Organizer.objects.get(user=self.request.user)
        except Organizer.DoesNotExist:
            return False
        return self.extra(organizer)


class OrganizerAdminPermission(OrganizerPermission):
    def extra(self, organizer):
        return organizer.admin


class OrganizerActivityPermission(OrganizerPermission):
    def extra(self, organizer):
        activity_id = self.kwargs.get("id", '')
        activity = get_object_or_404(Activity, pk=activity_id)
        return activity.organized_by_id == organizer.organization_id


class ClientPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.client.is_verified
