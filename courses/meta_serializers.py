from rest_framework import serializers

from .models import Lecturer, Lesson, Course


class LecturerMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lecturer
        fields = 'href',


class LessonMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = 'href',


class CourseMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = 'href',
