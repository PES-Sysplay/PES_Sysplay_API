from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from chat.models import Chat, Message
from user.mixins import OrganizerPermission


class ChatView(OrganizerPermission, TemplateView):
    template_name = 'chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search', '')
        organization = self.request.user.organizer.organization
        organization_ids = organization.organizer_set.values_list('user_id', flat=True)
        chats = Chat.objects.filter(activity__organized_by_id=organization)
        if search:
            chats = chats.filter(Q(activity__name__icontains=search) | Q(client__user__username__icontains=search))
        chats = list(chats)
        chats.sort(key=lambda x: x.last_message.date.timestamp() + (
            datetime.now().timestamp() if x.last_message.user_id not in organization_ids else 0), reverse=True)
        context.update({
            'chats_list': chats,
            'search': search,
        })
        return context


class ChatIndividualView(ChatView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_id = self.kwargs.get('id', None)
        if not chat_id:
            raise Http404
        chat = get_object_or_404(Chat, id=chat_id)
        context.update({
            'actual_chat': chat,
        })
        return context

    def post(self, request, id):
        message = request.POST.get('message', None)
        if not id:
            raise Http404
        chat = get_object_or_404(Chat, id=id)
        if message:
            if len(message) <= 1000:
                Message(user=request.user, text=message, chat=chat).save()
            else:
                messages.error(request, 'El número maximo de caracteres son 1000', extra_tags='danger')
        return redirect(reverse('chat_individual', args=[id]))
