from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EnrollmentStatus, Notification

@receiver(post_save, sender=EnrollmentStatus)
def create_notification(sender, instance, created, **kwargs):
    print(1)
    # if not created:
    Notification.objects.create(
        user=instance.student,
        message=f"Ваш статус изменился на: {instance.get_status_display()}",
    )