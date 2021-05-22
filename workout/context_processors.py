from chat.models import Chat


def get_chat_context_processor(request):
    context = {}
    if not request.user.is_authenticated:
        return context
    organization = request.user.organizer.organization
    chats = Chat.objects.filter(activity__organized_by_id=organization)
    organization_ids = organization.organizer_set.values_list('user_id', flat=True)
    context.update({
        'organization_ids': organization_ids,
    })
    news = 0
    for chat in chats:
        if chat.last_message.user_id not in organization_ids:
            news += 1
    context.update({'new_chats': news})
    return context
