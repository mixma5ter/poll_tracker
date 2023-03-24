from django.urls import path, include
from . import views

app_name = 'contests'

urlpatterns = [
    # Список конкурсов
    path('', views.contests_list, name='contest_list'),
    # Просмотр конкурса (описание, выбор действий)
    path('<int:contest_id>/', views.contest_detail, name='contest_detail'),
    # Результаты конкурса (таблица результатов, выбор действий)
    path('<int:contest_id>/result/', views.contest_result, name='contest_result'),
    # Этап голосования
    path('<int:contest_id>/<int:contest_track_id>/<int:stage_id>/', views.contest_stage, name='contest_stage'),
    # Страница ошибки
    path('error/', views.contest_error, name='contest_error'),
]
