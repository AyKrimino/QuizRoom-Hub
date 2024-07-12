import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import StudentProfile
from classroom.models import Classroom


class Quiz(models.Model):
    id = models.UUIDField(_("Quiz id"), primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Quiz title"), max_length=200)
    content = models.TextField(_("Quiz content"), null=True, blank=True)
    created_at = models.DateTimeField(_("Quiz created at"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Quiz updated at"), auto_now=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="quizzes",
                                  verbose_name=_("Classroom"))

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}-{self.classroom.name}"


class Question(models.Model):
    id = models.UUIDField(_("Question id"), primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(_("Question description"))
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions", verbose_name=_("Quiz"))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return f"{self.description[:10]}..."


class Answer(models.Model):
    id = models.UUIDField(_("Answer id"), primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(_("Answer description"))
    is_valid = models.BooleanField(_("Answer validity"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name=_("Question"))

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return f"{self.description[:10]}"


class StudentAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name=_("Student"),
                                related_name="student_answers")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name=_("Answer"))

    class Meta:
        verbose_name = _("Student Answer")
        verbose_name_plural = _("Student Answers")
        constraints = [
            models.UniqueConstraint(
                fields=["student", "answer"],
                name="student-answer",
            )
        ]

    def __str__(self):
        return f"{self.student}-{self.answer}"


class StudentQuiz(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="submitted_quizzes",
                                verbose_name=_("Student"))
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="student_answers", verbose_name=_("Quiz"))
    mark = models.DecimalField(_("Mark"), max_digits=5, decimal_places=2)
    answered_at = models.DateTimeField(_("Answered at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Student quiz relation")
        verbose_name_plural = _("Student quiz relations")
        ordering = ("-mark", "-answered_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["student", "quiz"],
                name="student-quiz",
            ),
        ]

    def __str__(self):
        return f"{str(self.student)}-{str(self.quiz)} -> {self.mark}"
