from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CallingTask(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Revoked', 'Revoked'),
    ]

    counsellor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calling_tasks'
    )

    counsellor_name_snapshot = models.CharField(
        max_length=150,
        blank=True
    )

    reg_no = models.CharField(
        max_length=100,
        blank=True
    )

    reference = models.CharField(
        max_length=150,
        blank=True
    )

    candidate_name = models.CharField(
        max_length=150
    )

    mobile = models.CharField(
        max_length=10
    )

    assigned_date = models.DateField(
        default=timezone.localdate
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    candidate = models.OneToOneField(
        'students.Candidate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calling_task'
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            '-assigned_date',
            '-id'
        ]

    def __str__(self):
        return (
            f'{self.candidate_name} - '
            f'{self.mobile}'
        )

    def save(self, *args, **kwargs):
        if self.counsellor_id:
            self.counsellor_name_snapshot = (
                self.counsellor.get_full_name()
                or self.counsellor.username
            )
        super().save(*args, **kwargs)

    @property
    def is_completed(self):
        return self.status == 'Completed'
    
