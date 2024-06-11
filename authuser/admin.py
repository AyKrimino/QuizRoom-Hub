from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "first_name", "last_name", "is_teacher", "is_staff", "is_superuser",)
    list_filter = ("is_teacher", "is_staff", "is_superuser",)
    fieldsets = (
        (None, {"fields": ("email", "password",)}),
        (_("User info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser", "is_active", "is_teacher",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "is_teacher", "password1", "password2",),
        }),
    )
    search_fields = ("email", "first_name", "last_name",)
    ordering = ("-date_joined",)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
