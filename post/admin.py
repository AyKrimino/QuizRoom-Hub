from django.contrib import admin

from .models import CoursePost, Comment

admin.site.register(CoursePost)
admin.site.register(Comment)
