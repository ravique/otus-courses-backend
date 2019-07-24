from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from courses.tokens import account_activation_token


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    mail_subject = 'Activate your account.'

    message = render_to_string('courses/messages/account_activation.html', {
        'domain': str(get_current_site(request)),
        'user': user,
        'uid': uid,
        'token': token,
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email], from_email='example@example.com'
    )

    email.content_subtype = 'html'
    email.send()

    return True


def send_reminder_email(kwargs):
    lesson = kwargs.get('lesson')
    user = kwargs.get('user')

    mail_subject = 'Reminder about {}'.format(lesson.name)
    message = render_to_string('courses/messages/lesson_reminder.html', {
        'lesson_name': lesson.name,
        'lesson_date': lesson.date
    })

    email = EmailMessage(
        mail_subject, message, to=[user.email], from_email='example@example.com'
    )

    email.content_subtype = 'html'
    email.send()

    return True

