from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.student_list,
        name='student_list'
    ),

    path(
        'add/',
        views.add_candidate,
        name='add_candidate'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_candidate,
        name='edit_candidate'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_candidate,
        name='delete_candidate'
    ),
    path(
        'export/',
        views.export_candidates,
        name='export_candidates'
    ),

]