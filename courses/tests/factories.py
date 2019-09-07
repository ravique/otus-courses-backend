from django.contrib.auth.models import User
from django.utils.timezone import now

from courses.models import UserProperty, Course, Lecturer, Lesson


class Factory:
    @classmethod
    def create_verified_user(cls, username='Koala',
                             first_name='John',
                             last_name='Doe',
                             email='koala@example.com',
                             password=32768):

        cls.user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        cls.user_property = UserProperty.objects.create(
            user=cls.user,
            verified=True
        )
        cls.user.set_password(password)
        cls.user.save()

        return cls.user

    @classmethod
    def create_course(cls, name='TestCourse'):
        cls.course = Course.objects.create(
            name=name,
            description='D1',
            price='100'
        )

        return cls.course

    @classmethod
    def create_lecturer(cls, first_name='John',
                        last_name='Doe',
                        bio='Lorem Ipsum'):
        cls.lecturer = Lecturer.objects.create(
            first_name=first_name,
            last_name=last_name,
            bio=bio
        )
        return cls.lecturer

    @classmethod
    def create_lesson(cls, name='TestLesson1',
                      description='D1',
                      date=now(),
                      homework='Do someting',
                      course=None,
                      lecturer=None):
        cls.lesson = Lesson.objects.create(
            name=name,
            description=description,
            date=date,
            homework=homework,
            course=course,
            lecturer=lecturer

        )
        return cls.lesson
