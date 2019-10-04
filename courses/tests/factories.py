import factory
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now

from courses.models import UserProperty, Course, Lecturer, Lesson


class UserPropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProperty

    user = factory.SubFactory('courses.tests.factories.UserFactory')
    verified = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('word')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    user_property = factory.RelatedFactory(UserPropertyFactory, 'user')
    password = factory.PostGenerationMethodCall('set_password', 32768)


class LecturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lecturer

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    bio = factory.Faker('sentence')


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    price = factory.Faker('random_int')


class LessonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lesson

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    date = factory.Faker('date_time', tzinfo=timezone.get_current_timezone())
    homework = factory.Faker('sentence')
    lecturer = factory.SubFactory(
        LecturerFactory,
    )
    course = factory.SubFactory(
        CourseFactory,
    )
