from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django_tables2 import SingleTableView

from activity.models import Activity
from activity_action.models import ActivityJoined, ActivityReview
from activity_action.tables import CheckinTable, ReviewTable
from user.mixins import OrganizerActivityPermission, OrganizerPermission
from user.models import Client, Blocked


class CheckinView(OrganizerActivityPermission, SingleTableView):
    table_class = CheckinTable
    template_name = 'checkin.html'
    model = ActivityJoined

    def get_queryset(self):
        queryset = super().get_queryset()
        m_id = self.kwargs.get("id")
        queryset = queryset.filter(activity_id=m_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        m_id = self.kwargs.get("id")
        list_blocked = Blocked.objects.filter(organization__activity=m_id).values_list('client_id', flat=True)
        context.update({'id': m_id, 'blocked': list_blocked})
        return context

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


class BlockUserView(OrganizerActivityPermission, View):

    def get(self, request, id, uid):
        client = get_object_or_404(Client, user_id=uid)
        activity = get_object_or_404(Activity, id=id)
        organization = activity.organized_by
        if Blocked.objects.filter(organization=organization, client=client).exists():
            messages.error(request, 'Cliente ya está bloqueado', extra_tags='danger')
        else:
            Blocked(organization=organization, client=client).save()
            messages.success(request, 'Cliente bloqueado')
        return redirect(reverse('checkin-list', args=[id]))


class UnblockUserView(OrganizerActivityPermission, View):

    def get(self, request, id, uid):
        client = get_object_or_404(Client, user_id=uid)
        activity = get_object_or_404(Activity, id=id)
        organization = activity.organized_by
        if not Blocked.objects.filter(organization=organization, client=client).exists():
            messages.error(request, 'Cliente no estaba bloqueado', extra_tags='danger')
        else:
            Blocked.objects.get(organization=organization, client=client).delete()
            messages.success(request, 'Cliente desbloqueado')
        return redirect(reverse('checkin-list', args=[id]))


class ReviewsView(OrganizerActivityPermission, SingleTableView):
    template_name = 'reviews.html'
    table_class = ReviewTable
    model = ActivityReview

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(joined__activity_id=self.kwargs.get('id', 0))
        return queryset


class RemoveReview(OrganizerPermission, View):
    def get(self, request, id):
        review = get_object_or_404(ActivityReview, pk=id)
        activity_id = review.joined.activity_id
        if review.joined.activity.organized_by_id != request.user.organizer.organization_id:
            raise PermissionDenied()
        review.comment = ''
        review.save()
        messages.success(request, 'Comentario borrado correctamente')
        return redirect(reverse('reviews', args=[activity_id]))
