"""
poll_tracker URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # При переходе пользователя на главную страницу, отправляем его на страницу с конкурсами
    path('', RedirectView.as_view(url='contests/', permanent=False), name='index'),
    # Путь до страницы с конкурсами
    path('contests/', include('contests.urls', namespace='contests')),
    # Путь до админ-панели
    path('admin/', admin.site.urls),
]
