from workout.emails import Email


def send_email_invitation(sender, invited, password, url):
    context = {
        'sender': sender,
        'invited': invited,
        'password': password,
        'login_url': url,
    }
    Email('invite', context=context, list_mails=[invited.user.email]).send()
