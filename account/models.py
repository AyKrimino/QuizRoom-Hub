import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TeacherProfile(models.Model):
    id = models.UUIDField(_("Teacher id"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"),
                                related_name="teacher_profile")
    bio = models.TextField(_("Bio"), blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pictures/', blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(_("Years of Experience"), blank=True, null=True)

    class Meta:
        verbose_name = _("Teacher Profile")
        verbose_name_plural = _("Teacher Profiles")
        ordering = ("-years_of_experience", "date_of_birth",)

    def __str__(self):
        return str(self.user).split("@")[0]


class StudentProfile(models.Model):
    id = models.UUIDField(_("Student id"), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"),
                                related_name="student_profile")
    bio = models.TextField(_("Bio"), blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    profile_picture = models.ImageField(_("Profile Picture"), upload_to='profile_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = _("Student Profile")
        verbose_name_plural = _("Student Profiles")
        ordering = ("date_of_birth",)

    def __str__(self):
        return str(self.user).split("@")[0]
