from rest_framework import serializers

from .models import Lecturer, Lesson, Course


class LinkSerializer(serializers.ModelSerializer):
    href = serializers.CharField(source='get_absolute_url')


class LecturerMetaSerializer(LinkSerializer):
    class Meta:
        model = Lecturer
        fields = 'href',


class LessonMetaSerializer(LinkSerializer):
    # href = serializers.HyperlinkedIdentityField('courses:lesson-detail', lookup_field='pk')

    class Meta:
        model = Lesson
        fields = 'href',


class CourseMetaSerializer(LinkSerializer):
    class Meta:
        model = Course
        fields = 'href',

