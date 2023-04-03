from django.urls import path, include
from . import views
from .views import (ContestDetailView,
                    ContestsListView,
                    ContestResultView,
                    ContestStageView,
                    ScoreCreateView)

app_name = 'contests'  # namespace

urlpatterns = [
    # Список конкурсов
    path('', ContestsListView.as_view(), name='contest_list'),

    # Просмотр конкурса (описание, выбор действий)
    path('<int:contest_pk>/', ContestDetailView.as_view(), name='contest_detail'),

    # Результаты конкурса (таблица результатов, выбор действий)
    path('<int:contest_pk>/result/', ContestResultView.as_view(), name='contest_result'),

    # Страница выбора этапа конкурса
    path('<int:contest_pk>/<int:track_pk>/', ContestStageView.as_view(), name='contest_stage'),

    # Страница голосования
    path('<int:contest_pk>/<int:track_pk>/<int:stage_pk>/', ScoreCreateView.as_view(), name='contest_polling'),

    # Страница ошибки
    path('error/', views.contest_error, name='contest_error'),
]
