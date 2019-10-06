from django.contrib import admin

from .models import Lecturer, Lesson, Course, UserProperty, Score


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    pass


class ScoreInline(admin.StackedInline):
    model = Score


@admin.register(Lesson)
class LectionAdmin(admin.ModelAdmin):
    list_display = 'name', 'lecturer', 'date',
    inlines = ScoreInline,


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProperty)
class UserPropertyAdmin(admin.ModelAdmin):
    pass

