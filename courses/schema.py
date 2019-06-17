import graphene

from graphene_django.types import DjangoObjectType

from .models import Lesson, Course, Lecturer


class CourseType(DjangoObjectType):
    ''' Returns course object '''

    class Meta:
        model = Course


class LecturerType(DjangoObjectType):
    full_name = graphene.String()

    class Meta:
        model = Lecturer

    @staticmethod
    def resolve_full_name(parent, info, **kwargs):
        return parent.full_name()


class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson


class CreateLecturer(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    result_lecturer = graphene.Field(LecturerType)

    def mutate(self, info, first_name, last_name):
        try:
            lecturer = Lecturer.objects.create(first_name=first_name, last_name=last_name)
        except:
            return None
        else:
            return CreateLecturer(result_lecturer=lecturer)


class EditLecturer(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        first_name = graphene.String()
        last_name = graphene.String()

    result_lecturer = graphene.Field(LecturerType)

    def mutate(self, info, id, **kwargs):
        first_name = kwargs.get('first_name', None)
        last_name = kwargs.get('last_name', None)
        lecturer = Lecturer.objects.get(id=id)
        if first_name:
            lecturer.first_name = first_name
        if last_name:
            lecturer.last_name = last_name
        lecturer.save()

        return EditLecturer(result_lecturer=lecturer)


class Mutation:
    create_lecturer = CreateLecturer.Field()
    edit_lecturer = EditLecturer.Field()


class Query:
    all_lessons = graphene.List(LessonType)
    all_courses = graphene.List(CourseType)
    all_lecturers = graphene.List(LecturerType)

    course = graphene.Field(CourseType, id=graphene.Int())
    lecturer = graphene.Field(LecturerType, id=graphene.Int())
    lesson = graphene.List(LessonType, id=graphene.Int(), name=graphene.String())

    def resolve_all_lessons(parent, info, **kwargs):
        return Lesson.objects.all()

    def resolve_all_courses(parent, info, **kwargs):
        return Course.objects.all()

    def resolve_all_lecturers(parent, info, **kwargs):
        return Lecturer.objects.all()

    def resolve_course(parent, info, **kwargs):
        return Course.objects.get(id=kwargs.get('id'))

    def resolve_lecturer(parent, info, **kwargs):
        return Lecturer.objects.get(id=kwargs.get('id'))

    def resolve_lesson(parent, info, **kwargs):
        if 'id' in kwargs:
            return Lesson.objects.filter(id=kwargs.get('id'))
        if 'name' in kwargs:
            return Lesson.objects.filter(name=kwargs.get('name'))
        return None
