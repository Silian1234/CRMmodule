from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    firstName = models.CharField(max_length=150, null=True)
    lastName = models.CharField(max_length=150, null=True)
    fatherName = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True)
    stack = models.CharField(max_length=255, blank=True, null=True)
    portfolio = models.TextField(blank=True, null=True)
    contacts = models.TextField(blank=True, null=True)
    #requests = models.JSONField(default=list, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        group_name = self.groups.first().name if self.groups.exists() else "Нет группы"
        return f"{self.username} ({self.firstName} {self.lastName}) ({group_name})"


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=[('test', 'С тестом'), ('no_test', 'Без теста')])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    enrollment_deadline = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    telegram_chat_link = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to='event_pictures/', blank=True, null=True)
    hidden = models.BooleanField(default=False)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='led_events',
        null=True,
        blank=True
    )
    curator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='curated_events',
        null=True,
        blank=True
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='event_participants',
        blank=True
    )

    def __str__(self):
        return self.name

    def can_add_participant(self):
        current_count = self.participants.count()
        return current_count < self.capacity

    def add_participant(self, user):
        if not self.can_add_participant():
            raise ValueError("Превышено максимальное количество участников")
        self.participants.add(user)

class EnrollmentStatus(models.Model):
    STATUS_CHOICES = [
        ('data_submitted', 'Отправил(а) персональные данные'),
        ('test_passed', 'Прошёл(ла) тестирование'),
        ('added_to_chat', 'Добавлен(а) в организационный чат'),
        ('started', 'Приступил(а) к мероприятию'),
        ('test_failed', 'Не прошёл(ла) тестирование'),
        ('completed', 'Завершил(а) прохождение мероприятия'),
        ('removed', 'Удалён(а) с мероприятия'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"