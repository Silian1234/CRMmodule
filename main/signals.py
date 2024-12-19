from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from .models import EnrollmentStatus, Notification
from .telegram_bot import send_notification_to_user

@receiver(post_save, sender=EnrollmentStatus)
def create_notification(sender, instance, created, **kwargs):
    # Сигнал для создания уведомления при изменении EnrollmentStatus
    if created or not created:
        # Проверяем, менялся ли статус или новая запись (optional, в зависимости от логики)
        print("Создание уведомления")
        Notification.objects.create(
            user=instance.student,
            message=f"Ваш статус изменился на: {instance.get_status_display()}",
        )

@receiver(post_save, sender=Notification)
def notify_user_via_telegram(sender, instance, created, **kwargs):
    # Сигнал для отправки уведомления в Telegram при создании уведомления
    if created and instance.user and instance.user.contacts:
        print("Отправка уведомления в Telegram")
        # Вызываем асинхронную функцию через async_to_sync
        async_to_sync(send_notification_to_user)(instance.user.contacts, instance.message)
