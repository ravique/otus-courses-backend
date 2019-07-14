from datetime import datetime, timedelta

from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

from courses.messages import send_reminder_email

redis_connection = Redis()

queue = Queue(connection=redis_connection)
scheduler = Scheduler(connection=redis_connection)


def schedule_reminder_messages(user, course, time=timedelta(hours=3)):
    for lesson in course.lessons:
        remind_moment = lesson.date - time - timedelta(hours=3)  # Fix UTC for Moscow time
        scheduler.enqueue_at(remind_moment, send_reminder_email, kwargs={user: user, lesson: lesson})
