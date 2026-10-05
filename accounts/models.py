from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('Super Admin', 'Super Admin'),
        ('Admin', 'Admin'),
        ('Counsellor', 'Counsellor'),
        ('Trainer', 'Trainer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    contact_no = models.CharField(
        max_length=15,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f'{self.user.username} - {self.role}'