from django.contrib import admin

from .models import TeacherProfile, StudentProfile

admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
