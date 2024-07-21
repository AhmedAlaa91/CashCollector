from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('frozen', 'Frozen'),
    ]

    manager_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.pk}"