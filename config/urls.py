from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('students/', include('students.urls')),
    path('accounts/', include('accounts.urls')),
    path('calling/',include('calling.urls')),
]
