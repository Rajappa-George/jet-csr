from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path('training/batches/', views.training_placeholder, {'section': 'batches'}, name='training_batches'),
    path('training/sessions/', views.training_placeholder, {'section': 'sessions'}, name='training_sessions'),
    path('training/attendance/', views.training_placeholder, {'section': 'attendance'}, name='training_attendance'),
]
