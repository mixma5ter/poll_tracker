from django.urls import path, include
from . import views

app_name = 'contests'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Список конкурсов
    path('contests/', views.contests_list),
    # Просмотр конкурса
    path('contests/<int:contest_id>/', views.contest_detail, name='contest_detail'),
]
