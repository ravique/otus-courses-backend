from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers

from .meta_serializers import LessonMetaSerializer, LecturerMetaSerializer, CourseMetaSerializer
from .models import Lecturer, Lesson, Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'password', 'email',
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class CourseShortSerializer(serializers.ModelSerializer):
    links = CourseMetaSerializer()

    class Meta:
        model = Course
        fields = 'name', 'links',


class LessonShortSerializer(serializers.ModelSerializer):
    links = LessonMetaSerializer()

    class Meta:
        model = Lesson
        fields = 'name', 'links',


class LecturerShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    links = LecturerMetaSerializer()

    class Meta:
        model = Lecturer
        fields = 'name', 'links',


class LecturerSerializer(serializers.ModelSerializer):
    links = LecturerMetaSerializer()
    courses = CourseShortSerializer(many=True)

    class Meta:
        model = Lecturer
        fields = 'links', 'id', 'first_name', 'last_name', 'photo', 'bio', 'courses'


class LessonSerializer(serializers.ModelSerializer):
    links = LessonMetaSerializer()
    lecturer = LecturerShortSerializer()
    course = CourseShortSerializer()

    class Meta:
        model = Lesson
        fields = 'links', 'id', 'name', 'description', 'date', 'homework', 'course', 'lecturer',


class CourseSerializer(serializers.ModelSerializer):
    links = CourseMetaSerializer()
    lessons = LessonSerializer(many=True)
    lecturers = LecturerShortSerializer(many=True)

    class Meta:
        model = Course
        fields = 'links', 'id', 'start', 'finish', 'name', 'description', 'price', 'lessons', 'lecturers',
