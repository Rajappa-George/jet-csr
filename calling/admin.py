from django.contrib import admin

from .models import CallingTask


@admin.register(CallingTask)
class CallingTaskAdmin(admin.ModelAdmin):

    list_display = [
        'candidate_name',
        'mobile',
        'counsellor',
        'assigned_date',
        'status',
    ]

    list_filter = [
        'status',
        'assigned_date',
        'counsellor',
    ]

    search_fields = [
        'candidate_name',
        'mobile',
        'reg_no',
        'reference',
        'counsellor__username',
    ]