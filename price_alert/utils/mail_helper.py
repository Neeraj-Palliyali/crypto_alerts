from django.conf import settings
from django.core.mail import send_mail


def send_mails(subject, user_email, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email, ]
    try:
        status = send_mail( subject, message, email_from, recipient_list )
        return str(status)
    except Exception as e:
        return str(e)