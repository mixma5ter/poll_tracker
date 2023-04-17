from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContestResultJson

app_name = 'api'  # namespace

router_v1 = DefaultRouter()
router_v1.register(
    r'results/json/(?P<contest_id>\d+)',
    ContestResultJson,
    basename='results'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]