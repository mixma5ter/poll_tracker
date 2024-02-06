from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.models import APIClient
from core.utils import process_contest_data

from poll_tracker.settings import MEDIA_URL


class ContestResultJson(viewsets.ModelViewSet):
    """Отправка данных API клиенту."""

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
            item['contest__title'] = contest.title
            item['contest__track'] = track.title if track else ""
            item['contest__stage'] = stage.title if stage else ""
            if item['contestant__photo']:
                item['contestant__photo'] = f'http://{host}{MEDIA_URL}{item["contestant__photo"]}'
        return list(results)

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        return JsonResponse({'results': results})
