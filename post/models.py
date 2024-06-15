import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from classroom.models import Classroom

User = get_user_model()


class CoursePost(models.Model):
    id = models.UUIDField(_("Course id"), primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Course title"), max_length=200)
    content = models.TextField(_("Course content"))
    created_at = models.DateTimeField(_("Course created at"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Course updated at"), auto_now=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="courses",
                                  verbose_name=_("Classroom"))

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}-{self.classroom.name}"


class Comment(models.Model):
    id = models.UUIDField(_("Comment id"), primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(_("Comment content"))
    created_at = models.DateTimeField(_("Comment created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Comment updated at"), auto_now=True)
    post = models.ForeignKey(CoursePost, on_delete=models.CASCADE, related_name="comments",
                             verbose_name=_("Course post"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name=_("User"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.content[:10]}..."
