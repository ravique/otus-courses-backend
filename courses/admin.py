from django.contrib import admin

from .models import Lecturer, Lesson, Course, UserProperty


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LectionAdmin(admin.ModelAdmin):
    list_display = 'name', 'lecturer', 'date',


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProperty)
class UserPropertyAdmin(admin.ModelAdmin):
    pass
