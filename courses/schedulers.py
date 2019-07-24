import json
from datetime import timedelta

import django_rq

from courses.messages import send_reminder_email

lesson_scheduler = django_rq.get_scheduler('lesson_reminder')


def schedule_reminder_messages(user, course, time=timedelta(hours=3)):
    for lesson in course.lessons.all():
        remind_moment = lesson.date - time - timedelta(hours=3)  # Fix UTC for Moscow time
        job_description = json.dumps({'user': user.id, 'lesson': lesson.id})
        lesson_scheduler.enqueue_at(remind_moment, send_reminder_email,
                                    kwargs={'user': user, 'lesson': lesson},
                                    job_description=job_description
                                    )


def clear_reminder_messages(user, course):
    for lesson in course.lessons.all():
        all_schedules = lesson_scheduler.get_jobs()
        for job in all_schedules:
            job_description = json.loads(job.description)
            if job_description.get('user') == user.id \
                    and job_description.get('lesson') == lesson.id:
                lesson_scheduler.cancel(job)

