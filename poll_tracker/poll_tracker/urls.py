from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings

from brain_ring.views import brain_ring_page, get_current_question, submit_answer
from contests.views import IndexView
urlpatterns = [
    # главная страница
    path('', IndexView.as_view(), name='index'),
    # конкурсы
    path('contests/', include('contests.urls', namespace='contests')),
    # api
    path('api/', include('api.urls', namespace='api')),
    # админ-панель
    path('admin/', admin.site.urls),
    # smart_selects
    path('chaining/', include('smart_selects.urls')),
    # иконка админ панели
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),

    # brain-ring
    path('brainring/', brain_ring_page, name='brainring'),
    path('get-current-question/', get_current_question, name='get_current_question'),
    path('submit-answer/', submit_answer, name='submit_answer'),
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
