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
        return f"{self.firstName} {self.lastName} ({self.groups})"
