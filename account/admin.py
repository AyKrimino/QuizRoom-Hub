from django.contrib import admin

from .models import TeacherProfile, StudentProfile


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
