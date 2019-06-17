from django.contrib.auth.models import User
from django.db import models


class MetaMixin:
    @property
    def links(self):
        return self


class UserProperty(MetaMixin, models.Model):
    verified = models.BooleanField(default=False, verbose_name='Is verified')
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE, related_name='user_property')


class Lecturer(MetaMixin, models.Model):
    first_name = models.CharField(max_length=255, blank=True, verbose_name='First name')
    last_name = models.CharField(max_length=255, blank=True, verbose_name='Last name')
    photo = models.ImageField(upload_to='persons', blank=True, verbose_name='Lecturers photo')
    bio = models.TextField(blank=True, verbose_name='Lecturer bio')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def full_name(self):
        return self.__str__


class Course(MetaMixin, models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Course title')
    description = models.TextField(blank=True, verbose_name='Course description')
    price = models.PositiveIntegerField(blank=False, verbose_name='Course full price')
    lecturers = models.ManyToManyField(Lecturer, blank=False, related_name='courses', verbose_name='Course lecturers')
    students = models.ManyToManyField(User, blank=True, related_name='courses',
                                      verbose_name='Course students')

    def __str__(self):
        return self.name

    @property
    def start(self):
        return self.lessons.all().order_by('date').first().date

    @property
    def finish(self):
        return self.lessons.all().order_by('date').last().date


class Lesson(MetaMixin, models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Lesson title')
    description = models.TextField(blank=True, verbose_name='Lesson description')
    date = models.DateTimeField(blank=True, verbose_name='Lesson date')
    homework = models.TextField(blank=True, verbose_name='Lesson homework')
    lecturer = models.ForeignKey(Lecturer, blank=True, null=True, on_delete=models.SET_NULL, related_name='lections',
                                 verbose_name='Lesson speaker')
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.SET_NULL, related_name='lessons',
                               verbose_name='Course')

    def __str__(self):
        return self.name

# TODO: Pagination
