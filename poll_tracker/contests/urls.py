from django.urls import path, include
from . import views
from .views import (ContestDetailView,
                    ContestsListView,
                    ContestResultView,
                    ContestStageView,
                    add_score_view)

app_name = 'contests'  # namespace


urlpatterns = [
    # Список конкурсов
    path('<slug:judge_slug>/', ContestsListView.as_view(), name='contest_list'),

    # Просмотр конкурса (описание, выбор действий)
    path('<slug:judge_slug>/<int:contest_pk>/', ContestDetailView.as_view(), name='contest_detail'),

    # Результаты конкурса (таблица результатов, выбор действий)
    path('<slug:judge_slug>/<int:contest_pk>/result/', ContestResultView.as_view(), name='contest_result'),

    # Страница выбора этапа конкурса
    path('<slug:judge_slug>/<int:contest_pk>/<int:track_pk>/', ContestStageView.as_view(), name='contest_stage'),

    # Страница голосования
    path('<slug:judge_slug>/<int:contest_pk>/<int:track_pk>/<int:stage_pk>/', add_score_view, name='contest_polling'),

    # Страница ошибки
    path('error/', views.contest_error, name='contest_error'),
]
