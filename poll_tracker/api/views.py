from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.models import APIClient
from core.utils import process_contest_data

from poll_tracker.poll_tracker.settings import MEDIA_URL


class ContestResultJson(viewsets.ModelViewSet):
    """Отправка данных в VMix."""

    def get_queryset(self):
        client = get_object_or_404(APIClient, title=self.kwargs.get('value'))
        contest = client.contest
        if not contest:
            return None

        track = client.track
        stage = client.stage
        results = process_contest_data(contest, track, stage)
        host = self.request.get_host()
        for item in results:
            if item['contestant__photo']:
                item['contestant__photo'] = f'http://{host}{MEDIA_URL}{item["contestant__photo"]}'
            item['contest'] = contest.title
        return list(results)

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        return JsonResponse({'results': results})
