from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import TeacherProfile, StudentProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser and not instance.is_staff:
            if not hasattr(instance, "teacher_profile") and not hasattr(instance,
                                                                        "student_profile"):
                if instance.is_teacher:
                    TeacherProfile.objects.create(user=instance)
                else:
                    StudentProfile.objects.create(user=instance)
