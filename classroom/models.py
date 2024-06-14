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


class Classroom(models.Model):
    id = models.UUIDField(_("Classroom id"), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Classroom name"), max_length=200)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="classrooms",
                                verbose_name=_("Teacher"))
    created_at = models.DateTimeField(_("Classroom created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Classroom")
        verbose_name_plural = _("Classrooms")
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class StudentClassroom(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, verbose_name=_("Student"))
    classroom = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, verbose_name=_("Classroom"))
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True, blank=True)

    class Meat:
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

    class Meat:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return f"{self.description[:10]}..."


class Answer(models.Model):
    id = models.UUIDField(_("Answer id"), primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(_("Answer description"))
    is_valid = models.BooleanField(_("Answer validity"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name=_("Question"))


class StudentQuiz(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="submitted_quizzes",
                                verbose_name=_("Student"))
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="student_answers", verbose_name=_("Quiz"))
    mark = models.DecimalField(_("Mark"), max_digits=4, decimal_places=2)
