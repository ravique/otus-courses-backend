import json

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from courses.tests.factories import Factory
from courses.models import Course, Lesson, Lecturer
from courses.serializers import CourseSerializer, LessonSerializer, LecturerSerializer
from courses.views import LessonListView

client = Client()
factory = APIRequestFactory()


class CourseViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Factory.create_course(name='TestCourse1')
        Factory.create_course(name='TestCourse2')

    def test_CourseListView(self):
        response_from_view = client.get(reverse('course-list')).content
        response_from_url = client.get('/api/course/').content

        request = factory.get('/api/course/')
        serializer_context = {
            'request': Request(request),
        }

        courses = Course.objects.all()
        serializer = CourseSerializer(courses, context=serializer_context, many=True)
        test_data = JSONRenderer().render(
            {'links': {
                'href': str(get_current_site(request)) + request.path
            },
                'objects': serializer.data
            }
        )

        self.assertEqual(test_data, response_from_url, response_from_view)

    def test_CourseDetailView(self):
        response_from_view = client.get(reverse('course-detail', kwargs={'pk': 1})).content
        response_from_url = client.get('/api/course/1/').content

        request = factory.get('/api/course/')
        serializer_context = {
            'request': Request(request),
        }

        course = Course.objects.get(id=1)
        serializer = CourseSerializer(course, context=serializer_context)

        test_data = JSONRenderer().render(serializer.data)

        self.assertEqual(test_data, response_from_url)
        self.assertEqual(test_data, response_from_view)


class LessonViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.course = Factory.create_course(name='TestCourse1')
        cls.lecturer = Factory.create_lecturer()
        Factory.create_lesson(name='TestLesson1', course=cls.course, lecturer=cls.lecturer)
        Factory.create_lesson(name='TestLesson2', course=cls.course, lecturer=cls.lecturer)

    def test_LessonDetailView(self):
        response_from_view = client.get(reverse('lesson-detail', kwargs={'pk': 1})).content
        response_from_url = client.get('/api/lesson/1/').content

        request = factory.get('/api/lesson/1/')
        serializer_context = {
            'request': Request(request),
        }

        lesson = Lesson.objects.get(id=1)
        serializer = LessonSerializer(lesson, context=serializer_context)
        test_data = JSONRenderer().render(serializer.data)

        self.assertEqual(test_data, response_from_url, response_from_view)

    def test_LessonListView(self):
        response_from_view = client.get(reverse('lesson-list')).content
        response_from_url = client.get('/api/lesson/').content

        request = factory.get('/api/lesson/')
        serializer_context = {
            'request': Request(request),
        }

        lesson = Lesson.objects.all()
        serializer = LessonSerializer(lesson, context=serializer_context, many=True)

        test_data = JSONRenderer().render(
            {'links': {
                'href': str(get_current_site(request)) + request.path
            },
                'objects': serializer.data
            }
        )

        self.assertEqual(test_data, response_from_url)
        self.assertEqual(test_data, response_from_view)

    def test_LessonListView_with_params(self):
        lesson_list_view = LessonListView()
        request = factory.get('/api/lesson/?name=TestLesson2')
        lesson_list_view.request = Request(request)

        test_lesson = Lesson.objects.filter(name='TestLesson2')

        self.assertEqual(lesson_list_view.get_queryset().first(), test_lesson.first())


class LecturerViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.course = Factory.create_course()
        cls.lecturer = Factory.create_lecturer()
        Factory.create_lesson(course=cls.course, lecturer=cls.lecturer)

    def test_LecturerDetailView(self):
        response_from_view = client.get(reverse('lecturer-detail', kwargs={'pk': 1})).content
        response_from_url = client.get('/api/lecturer/1/').content

        request = factory.get('/api/lecturer/1/')
        serializer_context = {
            'request': Request(request),
        }

        lecturer = Lecturer.objects.get(id=1)
        serializer = LecturerSerializer(lecturer, context=serializer_context)
        test_data = JSONRenderer().render(serializer.data)

        self.assertEqual(test_data, response_from_url)
        self.assertEqual(test_data, response_from_view)

    def test_LecturerListView(self):
        response_from_view = client.get(reverse('lecturer-list')).content
        response_from_url = client.get('/api/lecturer/').content

        request = factory.get('/api/lecturer/')
        serializer_context = {
            'request': Request(request),
        }

        lesson = Lecturer.objects.all()
        serializer = LecturerSerializer(lesson, context=serializer_context, many=True)

        test_data = JSONRenderer().render(
            {'links': {
                'href': str(get_current_site(request)) + request.path
            },
                'objects': serializer.data
            }
        )

        self.assertEqual(test_data, response_from_url)
        self.assertEqual(test_data, response_from_view)


class RegisterTestCase(TestCase):
    def test_register_view_get(self):
        response_from_url = client.get('/api/register/')
        self.assertEqual(405, response_from_url.status_code)

    def test_register_view_post_good(self):
        request = {
            'username': 'Test',
            'password': 32768,
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/register/', data=request_json, content_type='application/json')

        user = User.objects.first()

        self.assertEqual(201, response_from_url.status_code)
        self.assertEqual(user.username, request['username'])
        self.assertEqual(user.email, request['email'])
        self.assertEqual(user.first_name, request['first_name'])
        self.assertEqual(user.last_name, request['last_name'])
        self.assertEqual(user.is_staff, False)

    def test_register_view_post_bad_email(self):
        request = {
            'username': 'Test',
            'password': 32768,
            'email': 'testexample.com'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/register/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)
        self.assertTrue('Error' in json.loads(response_from_url.content).keys())

    def test_register_view_post_no_password(self):
        request = {
            'username': 'Test',
            'email': 'testexample.com'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/register/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)
        self.assertTrue('Error' in json.loads(response_from_url.content).keys())

    def test_register_view_post_no_username(self):
        request = {
            'password': 32768,
            'email': 'test@example.com'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/register/', data=request_json, content_type='application/json')

        self.assertEqual(400, response_from_url.status_code)
        self.assertTrue('Error' in json.loads(response_from_url.content).keys())


class LoginTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Factory.create_verified_user()

    def test_login_success(self):
        request = {
            'username': 'Koala',
            'password': 32768
        }

        user = User.objects.get(username='Koala')

        request_json = json.dumps(request)
        response_from_url = client.post('/api/login/', data=request_json, content_type='application/json')
        response_json = json.loads(response_from_url.content)

        self.assertEqual(200, response_from_url.status_code)
        self.assertEqual(response_json['id'], user.id)
        self.assertEqual(response_json['username'], user.username)
        self.assertEqual(response_json['first_name'], user.first_name)
        self.assertEqual(response_json['last_name'], user.last_name)
        self.assertEqual(response_json['email'], user.email)

        self.assertTrue(user.is_authenticated)

        # Paranoid mode on
        session_key = response_from_url.cookies['sessionid'].value
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')

        self.assertEqual(user.id, int(uid))
        # /Paranoid mode off

    def test_login_no_username(self):
        request = {
            'password': 32768
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/login/', data=request_json, content_type='application/json')
        response_json = json.loads(response_from_url.content)

        self.assertEqual(400, response_from_url.status_code)
        self.assertTrue('Error' in response_json.keys())

    def test_login_no_password(self):
        request = {
            'username': 'Koala'
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/login/', data=request_json, content_type='application/json')
        response_json = json.loads(response_from_url.content)

        self.assertEqual(400, response_from_url.status_code)
        self.assertTrue('Error' in response_json.keys())

    def test_login_wrong_password(self):
        request = {
            'username': 'Koala',
            'password': 1024
        }

        request_json = json.dumps(request)
        response_from_url = client.post('/api/login/', data=request_json, content_type='application/json')
        response_json = json.loads(response_from_url.content)

        self.assertEqual(400, response_from_url.status_code)
        self.assertTrue('Error' in response_json.keys())


class RegisterOnCourseViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_password = 32768
        cls.user = Factory.create_verified_user(password=user_password)
        cls.course = Factory.create_course()
        client.login(username=cls.user.username, password=32768)

    def test_register_on_course_success(self):
        client.login(username=self.__class__.user.username, password=32768) # Test wont pass without it. Don't know why
        request_uri = '/api/course/{}/register/'.format(self.__class__.course.id)
        response_from_url = client.post(request_uri)
        response_json = json.loads(response_from_url.content)

        self.assertTrue('Success' in response_json.keys())
        self.assertEqual(201, response_from_url.status_code)

    def test_register_on_course_error_registered_already(self):

        self.__class__.course.students.add(self.__class__.user)
        self.__class__.course.save()

        request_uri = '/api/course/{}/register/'.format(self.__class__.course.id)
        response_from_url = client.post(request_uri)
        response_json = json.loads(response_from_url.content)

        self.assertTrue('Not modified' in response_json.keys())
        self.assertEqual(200, response_from_url.status_code)

    def test_register_on_course_error_no_course(self):
        request_uri = '/api/course/5/register/'
        response_from_url = client.post(request_uri)
        self.assertTrue(404, response_from_url.status_code)

    def test_register_on_course_error_user_not_logged_in(self):
        client.logout()

        request_uri = '/api/course/{}/register/'.format(self.__class__.course.id)
        response_from_url = client.post(request_uri)

        self.assertEqual(403, response_from_url.status_code)



