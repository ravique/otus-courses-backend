from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse

from rest_framework import serializers

from .meta_serializers import LessonMetaSerializer, LecturerMetaSerializer, CourseMetaSerializer
from .models import Lecturer, Lesson, Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username', 'password', 'email', 'first_name', 'last_name',
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
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


class LecturerSerializer(serializers.ModelSerializer):
    links = LecturerMetaSerializer()

    class Meta:
        model = Lecturer
        fields = 'links', 'id', 'first_name', 'last_name', 'bio'


class LecturerShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    links = LecturerMetaSerializer()

    class Meta:
        model = Lecturer
        fields = 'name', 'links'


class CourseShortSerializer(serializers.ModelSerializer):
    links = CourseMetaSerializer()

    class Meta:
        model = Course
        fields = 'name', 'links'


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

