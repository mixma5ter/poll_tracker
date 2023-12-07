from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from contests.models import Contest
from core.utils import process_contest_data
from poll_tracker.settings import MEDIA_URL


class ContestResultJson(viewsets.ModelViewSet):
    """Отправка данных в VMix."""

    def get_queryset(self):
        contest = get_object_or_404(Contest, pk=self.kwargs.get('contest_id'))

        # Получаем результаты конкурса
        results = process_contest_data(contest)
        host = self.request.get_host()
        for item in results:
            if item['contestant__photo']:
                item['contestant__photo'] = f'http://{host}{MEDIA_URL}{item["contestant__photo"]}'
            item['contest'] = contest.title
        return results

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        return JsonResponse({'results': results})
