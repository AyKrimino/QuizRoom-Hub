from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

from django.conf import settings


class TeacherProfile(models.Model):
    class Meta:
        verbose_name = _("Teacher Profile")
        verbose_name_plural = _("Teacher Profiles")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"),
                                related_name="teacher_profile")
    bio = models.TextField(_("Bio"), blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pictures/', blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(_("Years of Experience"), blank=True, null=True)

    def __str__(self):
        return str(self.user)


class StudentProfile(models.Model):
    class Meta:
        verbose_name = _("Student Profile")
        verbose_name_plural = _("Student Profiles")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"),
                                related_name="student_profile")
    bio = models.TextField(_("Bio"), blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return str(self.user)
