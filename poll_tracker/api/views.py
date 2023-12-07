from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.models import APIClient
from core.utils import process_contest_data


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
        return list(results)

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        return JsonResponse({'results': results})
