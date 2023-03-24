"""
poll_tracker URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('contests.urls', namespace='contests')),
    path('admin/', admin.site.urls),
]
