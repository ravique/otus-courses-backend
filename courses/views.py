from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from courses.messages import send_verification_email
from .serializers import UserSerializer, LoginSerializer, LecturerSerializer, LessonSerializer, CourseSerializer, \
    AccountSerializer, UserPropertySerializer

from .models import Lecturer, Lesson, Course, UserProperty
from .tokens import account_activation_token


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class RegisterView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            UserProperty.objects.create(user=user)
            if send_verification_email(request, user):
                return Response(user_serializer.data)
        return Response(user_serializer.errors)


class LoginView(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.user_property.verified:
                return Response({'error': 'Login failed: Confirm Email first'})

            login(request, user)
            return Response(UserSerializer(user).data)

        return Response(serializer.errors)


class AccountView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = IsAuthenticated,

    def get(self, request):
        user_serializer = AccountSerializer(request.user, context={'request': request})
        user_property_serializer = UserPropertySerializer(request.user.user_property)
        user_data = user_serializer.data
        user_data.update(user_property_serializer.data)

        return Response(user_data)
    

class AccountVerificationView(APIView):
    permission_classes = AllowAny,

    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid', None)
        token = request.GET.get('token', None)

        if not uid or not token:
            return Response({'error': 'No uid or token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            if user.user_property.verified:
                return Response({'info': 'User is already verified'}, status=status.HTTP_304_NOT_MODIFIED)
            user.user_property.verified = True
            user.user_property.save()
            return Response({'ok': 'Your email was verified'})

        return Response({'error': 'Invalid user or token'}, status=status.HTTP_400_BAD_REQUEST)


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
        return Response({'links': {'href': str(get_current_site(request)) + request.path},
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
