from workout.emails import Email


def send_email_verification(url, client):
    context = {
        'client': client,
        'url': url,
    }
    Email('verification', context=context, list_mails=[client.user.email]).send()
