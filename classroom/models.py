import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import TeacherProfile, StudentProfile


class Classroom(models.Model):
    id = models.UUIDField(_("Classroom id"), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Classroom name"), max_length=200, blank=False, null=False)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="classrooms",
                                verbose_name=_("Teacher"))
    created_at = models.DateTimeField(_("Classroom created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Classroom")
        verbose_name_plural = _("Classrooms")
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError("The name field cannot be blank or null.")
        super().save(*args, **kwargs)


class StudentClassroom(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name=_("Student"))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_("Classroom"))
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Student Classroom relation"
        verbose_name_plural = "Student Classroom relations"
        ordering = ("-date_joined",)
        constraints = [
            models.UniqueConstraint(
                fields=["student", "classroom"],
                name="student-classroom",
            ),
        ]

    def __str__(self):
        return f"{self.student}-{self.classroom.name}"
