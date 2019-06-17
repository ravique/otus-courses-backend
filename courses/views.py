from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from .serializers import UserSerializer, LoginSerializer, LecturerSerializer, LessonSerializer, CourseSerializer, \
    AccountSerializer

from .models import Lecturer, Lesson, Course
from django.conf import settings


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class RegisterView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response(UserSerializer(user).data)

        return Response(serializer.errors)


class AccountView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = IsAuthenticated,

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, request):
        logout(request)
        return Response()


class RegisterOnCourseView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        user = request.user

        if user not in course.students.all():
            user.courses.add(course)
            message = {"Success": "User {} successfully registered on course {}".format(user, course)}
            return Response(message, status=status.HTTP_201_CREATED)

        message = {"Not modified": "User {} is already registered on course {}".format(user, course)}
        return Response(message, status=status.HTTP_304_NOT_MODIFIED)


class AddLinksListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        objects = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(objects, many=True, context={'request': self.request})
        return Response({'links': {'href': settings.DOMAIN + request.path},
                         'objects': data.data})

    lookup_field = 'id'


class LecturerListView(AddLinksListView):
    permission_classes = AllowAny,
    queryset = Lecturer.objects.prefetch_related('courses', 'lections').all()
    serializer_class = LecturerSerializer


class LecturerDetailView(generics.RetrieveAPIView):
    permission_classes = AllowAny,
    queryset = Lecturer.objects.prefetch_related('courses', 'lections').all()
    serializer_class = LecturerSerializer


class LessonListView(AddLinksListView):
    permission_classes = AllowAny,
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = Lesson.objects.all().select_related('course', 'lecturer')

        params = dict(self.request.query_params)
        date = params.get('date', None)
        if date:
            params['date__date'] = params.pop('date')

        kwargs = dict()

        for k, v in params.items():
            if k in ('date', 'id', 'name', 'course__name'):
                if len(v) > 1:
                    kwargs[k + '__in'] = v
                else:
                    kwargs[k] = ''.join(v)

        if kwargs:
            queryset = Lesson.objects.filter(**kwargs).select_related('course', 'lecturer')
        return queryset


class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = AllowAny,
    queryset = Lesson.objects.select_related('course', 'lecturer').all()
    serializer_class = LessonSerializer


class CourseListView(AddLinksListView):
    permission_classes = AllowAny,
    queryset = Course.objects.prefetch_related('lessons__lecturer', 'lecturers').all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = AllowAny,
    queryset = Course.objects.prefetch_related('lessons__lecturer', 'lecturers').all()
    serializer_class = CourseSerializer
