from django.db import models
from django.contrib.auth.models import User


class Candidate(models.Model):

    STATUS_CHOICES = [
        ('Interested', 'Interested'),
        ('Non-Interested', 'Non-Interested'),
        ('Yet to Confirm', 'Yet to Confirm'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    ]

    QUALIFICATION_CHOICES = [
        ('Below 5', 'Below 5'),
        ('5-9', '5-9'),
        ('10th', '10th'),
        ('12th', '12th'),
        ('Diploma', 'Diploma'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
    ]

    LOCATION_CHOICES = [
        (
            'Theru Veerapandiya Puram',
            'Theru Veerapandiya Puram'
        ),
        (
            'A. KumaraReddiyapuram',
            'A. KumaraReddiyapuram'
        ),
        (
            'T. Kumaragiri',
            'T. Kumaragiri'
        ),
        (
            'Milavittan',
            'Milavittan'
        ),
        (
            'Silverpuram',
            'Silverpuram'
        ),
        (
            'Pandarampatti',
            'Pandarampatti'
        ),
        (
            'Therespuram',
            'Therespuram'
        ),
        (
            'Anna Colony',
            'Anna Colony'
        ),
        (
            'Inigo Nagar',
            'Inigo Nagar'
        ),
        (
            'Others',
            'Others'
        ),
    ]

    COURSE_CHOICES = [
        (
            'Tailoring & Fashion Design',
            'Tailoring & Fashion Design'
        ),
        (
            'Computer / Tally / Accounts',
            'Computer / Tally / Accounts'
        ),
        (
            'Beauty & Wellness',
            'Beauty & Wellness'
        ),
        (
            'Retail & Sales',
            'Retail & Sales'
        ),
        (
            'Electrician',
            'Electrician'
        ),
        (
            'Fitter / Welder',
            'Fitter / Welder'
        ),
        (
            'Industrial Safety',
            'Industrial Safety'
        ),
        (
            'Logistics & Warehousing',
            'Logistics & Warehousing'
        ),
        (
            'Solar Technician',
            'Solar Technician'
        ),
        (
            'Driving (LMV / HMV)',
            'Driving (LMV / HMV)'
        ),
        (
            'Healthcare Assistant',
            'Healthcare Assistant'
        ),
        (
            'Hospitality',
            'Hospitality'
        ),
        (
            'Mobile Repair',
            'Mobile Repair'
        ),
        (
            'Fish Processing & Value Addition',
            'Fish Processing & Value Addition'
        ),
        (
            'Spoken English',
            'Spoken English'
        ),
    ]

    SKILL_PREFERENCE_CHOICES = [
        (
            'Fresh Skills Required',
            'Fresh Skills Required'
        ),
        (
            'Skilled only Certificate required',
            'Skilled only Certificate required'
        ),
    ]

    enquiry_date = models.DateField()

    counsellor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='counselled_candidates'
    )

    candidate_name = models.CharField(
        max_length=150
    )

    contact_no = models.CharField(
        max_length=10
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    qualification = models.CharField(
        max_length=30,
        choices=QUALIFICATION_CHOICES,
        blank=True
    )

    guardian_name = models.CharField(
        max_length=150,
        blank=True
    )

    location = models.CharField(
        max_length=100,
        choices=LOCATION_CHOICES,
        blank=True
    )

    other_location = models.CharField(
        max_length=150,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    course_interested = models.CharField(
        max_length=100,
        choices=COURSE_CHOICES,
        blank=True
    )

    family_annual_income = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    skill_preference = models.CharField(
        max_length=50,
        choices=SKILL_PREFERENCE_CHOICES,
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
        ordering = [
            '-enquiry_date',
            '-id'
        ]

    def __str__(self):
        return self.candidate_name