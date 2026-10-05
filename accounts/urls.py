from django.urls import path

from . import views


urlpatterns = [

    path(
        'assign-tasks/',
        views.assign_tasks,
        name='assign_tasks'
    ),

    path(
        'assign-tasks/task/<int:pk>/edit/',
        views.edit_call_task,
        name='edit_call_task'
    ),

    path(
        'assign-tasks/task/<int:pk>/transfer/',
        views.transfer_call_task,
        name='transfer_call_task'
    ),

    path(
        'assign-tasks/task/<int:pk>/revoke/',
        views.revoke_call_task,
        name='revoke_call_task'
    ),

    path(
        '',
        views.user_list,
        name='user_list'
    ),

    path(
        'add/',
        views.add_user,
        name='add_user'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_user,
        name='edit_user'
    ),

    path(
        'reset-password/<int:pk>/',
        views.reset_password,
        name='reset_password'
    ),

    path(
        'toggle-status/<int:pk>/',
        views.toggle_user_status,
        name='toggle_user_status'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_user,
        name='delete_user'
    ),

    path(
        'preview-calls/<int:pk>/',
        views.preview_call_upload,
        name='preview_call_upload'
    ),

    path(
        'assign-calls/<int:pk>/',
        views.assign_calls,
        name='assign_calls'
    ),

]
