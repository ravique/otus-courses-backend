from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from courses.tokens import account_activation_token


def send_email(email):
    email.send()


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    mail_subject = 'Activate your account'
    current_site = str(get_current_site(request))
    activation_uri = 'https://{}{}?uid={}&token={}'.format(current_site,
                                                           reverse('account-verification'),
                                                           uid,
                                                           token
                                                           )

    message = render_to_string('courses/messages/account_activation.html', {
        'user': user,
        'activation_uri': activation_uri
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email], from_email=settings.EMAIL_HOST_USER
    )

    email.content_subtype = 'html'
    send_email(email)

    return email


def send_reminder_email(kwargs):
    lesson = kwargs.get('lesson')
    user = kwargs.get('user')
    mail_subject = 'Reminder about {}'.format(lesson.name)
    message = render_to_string('courses/messages/lesson_reminder.html', {
        'user': user,
        'lesson_name': lesson.name,
        'lesson_date': lesson.date
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email], from_email=settings.EMAIL_HOST_USER
    )

    email.content_subtype = 'html'

    send_email(email)

    return email
