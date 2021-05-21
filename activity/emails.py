from workout.emails import Email


def send_email_activity_changed(old, new):
    fields = {'start_date': 'Fecha', 'start_time': 'Hora', 'duration': 'Duración', 'normal_price': 'Precio normal',
              'member_price': 'Precio miembros', 'number_participants': 'Número de participantes',
              'location': 'Ubicación'}
    changes = {}
    for field, name in fields.items():
        old_field = getattr(old, field)
        new_field = getattr(new, field)
        if old_field != new_field:
            changes[name] = (old_field, new_field)
    if changes:
        emails = old.activityjoined_set.filter(client__email=True).values_list('client__user__email', flat=True)
        context = {'changes': changes, 'activity': new}
        Email('activity_changed', context=context, list_mails=emails).send()


def send_email_activity_cancelled(activity):
    emails = activity.activityjoined_set.filter(client__email=True).values_list('client__user__email', flat=True)
    context = {'activity': activity}
    Email('activity_cancelled', context=context, list_mails=emails).send()
