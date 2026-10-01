from django.db import models


class Candidate(models.Model):

    STATUS_CHOICES = [
        ('Interested', 'Interested'),
        ('Wait for Confirmation', 'Wait for Confirmation'),
        ('Not-Interested', 'Not-Interested'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    enquiry_date = models.DateField()

    candidate_name = models.CharField(
        max_length=150
    )

    contact_no = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    dob = models.DateField(
        null=True,
        blank=True
    )

    qualification = models.CharField(
        max_length=150,
        blank=True
    )

    guardian_name = models.CharField(
        max_length=150,
        blank=True
    )

    guardian_contact_no = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES
    )

    remark = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-enquiry_date', '-id']

    def __str__(self):
        return self.candidate_name