from workout.emails import Email


def send_email_verification(url, client):
    context = {
        'client': client,
        'url': url,
    }
    Email('verification', context=context, list_mails=[client.user.email]).send()


def send_remainder_email(activity):
    context = {
        'activity': activity,
    }
    user_favorites = set(activity.favoriteactivity_set.all().values_list('client__user__email', flat=True))
    user_joined = set(activity.activityjoined_set.all().values_list('client__user__email', flat=True))
    emails = list(user_favorites - user_joined)
    if len(emails) != 0:
        Email('reminder', context=context, list_mails=emails).send()
