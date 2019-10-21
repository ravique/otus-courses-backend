from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status

from courses.messages import send_verification_email
from courses.schedulers import schedule_reminder_messages, clear_reminder_messages
from .serializers import UserSerializer, LoginSerializer, LecturerSerializer, LessonSerializer, CourseSerializer, \
    AccountSerializer, UserPropertySerializer, StudentSerializer

from .models import Lecturer, Lesson, Course, UserProperty, Score
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
            try:
                send_verification_email(request, user)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = AllowAny,

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if not user.user_property.verified:
                return Response({'errors': {'non_field_errors': ['Login failed. Confirm email first']}},
                                status=status.HTTP_400_BAD_REQUEST)

            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = IsAuthenticated,

    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request):
        user_serializer = AccountSerializer(request.user, context={'request': request})
        user_property_serializer = UserPropertySerializer(request.user.user_property)
        user_data = user_serializer.data
        user_data.update(user_property_serializer.data)

        return Response(user_data)

    def post(self, request):
        user_serializer = AccountSerializer(
            data=request.data,
            instance=request.user,
            context={'request': request}
        )
        user_property_serializer = UserPropertySerializer(
            data=request.data,
            instance=request.user,
        )
        if user_property_serializer.is_valid() and user_serializer.is_valid():
            user_serializer.update(instance=request.user,
                                   validated_data=user_serializer.validated_data)

            user_property_serializer.update(instance=request.user.user_property,
                                            validated_data=user_property_serializer.validated_data)

            user_serializer = AccountSerializer(request.user, context={'request': request})
            user_property_serializer = UserPropertySerializer(request.user.user_property)
            user_data = user_serializer.data
            user_data.update(user_property_serializer.data)

            return Response(user_data)

        user_property_serializer.is_valid()
        user_serializer.is_valid()
        user_serializer_errors = user_serializer.errors
        user_serializer_errors.update(user_property_serializer.errors)

        return Response({'errors': user_serializer_errors}, status=status.HTTP_400_BAD_REQUEST)


class AccountVerificationView(APIView):
    permission_classes = AllowAny,

    def get(self, request, *args, **kwargs):
        uid = request.GET.get('uid', None)
        token = request.GET.get('token', None)

        if not uid or not token:
            return Response({'errors': ['No uid or token provided']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = urlsafe_base64_decode(uid)
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            if user.user_property.verified:
                return Response({'Info': 'User email was already verified'}, status=status.HTTP_304_NOT_MODIFIED)
            user.user_property.verified = True
            user.user_property.save()
            return Response({'Success': 'User email was verified'})

        return Response({'errors': ['Invalid user or token']}, status=status.HTTP_400_BAD_REQUEST)


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

        if not course:
            error_message = {'errors': ['Course not found']}
            return Response(error_message, status=status.HTTP_404_NOT_FOUND)

        if user not in course.students.all():
            user.courses.add(course)
            success_message = {'Success': 'User {} successfully registered on course {}'.format(user, course)}

            schedule_reminder_messages(user=user, course=course)
            return Response(success_message, status=status.HTTP_201_CREATED)

        info_message = {'Not modified': 'User {} is already registered on course {}'.format(user, course)}
        return Response(info_message, status=status.HTTP_200_OK)


class UnRegisterOnCourseView(APIView):
    authentication_classes = CsrfExemptSessionAuthentication,
    permission_classes = IsAuthenticated,

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        user = request.user

        if not course:
            message = {'errors': ['Course not found']}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        if user in course.students.all():
            user.courses.remove(course)
            clear_reminder_messages(user, course)
            message = {'Success': 'User {} successfully unregistered on course {}'.format(user, course)}
            return Response(message, status=status.HTTP_201_CREATED)

        message = {'Not modified': 'User {} was not registered on course {}'.format(user, course)}
        return Response(message, status=status.HTTP_200_OK)


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


class TableView(APIView):
    serializer_class = StudentSerializer

    def get(self, request):

        if not request.user.lecturer:
            return Response({'errors': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)

        lecturers_students = User.objects.filter(
            scores__in=Score.objects.filter(lecturer=request.user.lecturer)
        ).distinct()

        serializer = StudentSerializer(lecturers_students, many=True)

        return Response(serializer.data)





