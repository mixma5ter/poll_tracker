from django.urls import path

from .views import ContestResultJson

app_name = 'api'  # namespace

urlpatterns = [
    path('<str:value>/', ContestResultJson.as_view({'get': 'list'}), name='results'),
]
