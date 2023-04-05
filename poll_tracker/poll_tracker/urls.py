"""
poll_tracker URL Configuration
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings

from contests.views import index

urlpatterns = [
    # Главная страница
    path('', index, name='index'),
    # Путь до страницы с конкурсами
    path('contests/', include('contests.urls', namespace='contests')),
    # Путь до админ-панели
    path('admin/', admin.site.urls),
    # Путь для smart_selects
    path('chaining/', include('smart_selects.urls')),
    # Путь до иконки админ панели
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]

# Обработчики страниц ошибок
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'
handler403 = 'core.views.permission_denied'

# Правило для режима отладки DjDT и загрузки медиа
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
