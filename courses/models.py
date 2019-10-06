from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class MetaMixin:
    @property
    def links(self):
        return self


class UserProperty(MetaMixin, models.Model):
    verified = models.BooleanField(default=False, verbose_name='Is verified')
    avatar = models.ImageField(null=True, blank=True, upload_to='images/user/avatar', verbose_name='User avatar')
    birthdate = models.DateField(null=True, blank=True, verbose_name='User birthdate')

    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE, related_name='user_property')

    @property
    def average_score(self):
        return Score.objects.filter(student=self.user).aggregate(Avg('rate')).get('rate__avg')

    @property
    def full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def __str__(self):
        return self.user.username


class Lecturer(MetaMixin, models.Model):
    first_name = models.CharField(max_length=255, blank=True, verbose_name='First name')
    last_name = models.CharField(max_length=255, blank=True, verbose_name='Last name')
    photo = models.ImageField(upload_to='persons', blank=True, verbose_name='Lecturers photo')
    bio = models.TextField(blank=True, verbose_name='Lecturer bio')

    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='lecturer')

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


SCORES = (
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class Score(MetaMixin, models.Model):
    rate = models.PositiveIntegerField(choices=SCORES, max_length=1, blank=False, verbose_name='Score')
    lecturer = models.ForeignKey(Lecturer, blank=False, null=False, on_delete=models.CASCADE, related_name='scores',
                                 verbose_name='Lecturer')
    student = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='scores')
    lesson = models.ForeignKey(Lesson, blank=False, null=False, on_delete=models.CASCADE, related_name='scores')

    def __str__(self):
        return str(self.rate)

