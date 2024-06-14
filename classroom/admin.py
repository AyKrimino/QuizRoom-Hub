from django.contrib import admin

from .models import (TeacherProfile, StudentProfile, StudentClassroom, StudentQuiz, Quiz, Classroom, CoursePost,
                     Question, Answer, Comment)


class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "years_of_experience",)
    list_filter = ("years_of_experience", "date_of_birth",)
    search_fields = ("user", "id",)
    ordering = ("-years_of_experience", "date_of_birth",)


class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth",)
    list_filter = ("date_of_birth",)
    search_fields = ("user", "id",)
    ordering = ("date_of_birth",)


admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Classroom)
admin.site.register(StudentClassroom)
admin.site.register(CoursePost)
admin.site.register(Comment)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StudentQuiz)
