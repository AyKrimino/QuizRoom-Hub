from django.db.models.signals import post_save
from django.dispatch import receiver

from classroom.models import TeacherProfile, StudentProfile
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser and not instance.is_staff:
            if not hasattr(instance, "teacher_profile") and not hasattr(instance,
                                                                        "student_profile"):  # User doesn't have a profile yet
                if instance.is_teacher:
                    TeacherProfile.objects.create(user=instance)
                else:
                    StudentProfile.objects.create(user=instance)
