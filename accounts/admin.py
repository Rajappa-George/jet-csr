from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'role',
        'contact_no',
        'created_at',
    )

    list_filter = (
        'role',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'contact_no',
    )