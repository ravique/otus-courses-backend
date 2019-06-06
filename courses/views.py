from datetime import datetime

from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from .serializers import UserSerializer, LoginSerializer, LecturerSerializer, LessonSerializer, CourseSerializer
from .models import Lecturer, Lesson, Course


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data['user']
        login(request, user)
        return Response(UserSerializer(user).data)


class AccountView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response()


class RegisterOnCourseView(APIView):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        user = request.user

        if user not in course.students.all():
            user.courses.add(course)
            message = {"Success": "User {} successfully registered on course {}".format(user, course)}
            return Response(message, status=status.HTTP_201_CREATED)

        message = {"Not modified": "User {} is already registered on course {}".format(user, course)}
        return Response(message, status=status.HTTP_304_NOT_MODIFIED)


class LecturerListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.all()


class LecturerDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.all()


class LessonListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LessonSerializer

    def get_queryset(self):
        queryset = Lesson.objects.all()

        params = dict(self.request.query_params)
        date = params.get('date', None)
        if date:
            params['date__date'] = params.pop('date')

        kwargs = dict()

        for k, v in params.items():
            if len(v) > 1:
                kwargs[k + '__in'] = v
            else:
                kwargs[k] = ''.join(v)

        if params:
            queryset = Lesson.objects.filter(**kwargs)
        return queryset


class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class CourseListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
