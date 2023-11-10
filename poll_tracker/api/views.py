from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from contests.models import Contest
from poll_tracker.settings import MEDIA_URL


class ContestResultJson(viewsets.ModelViewSet):
    """Отправка данных в VMix."""

    def get_queryset(self):
        contest = get_object_or_404(Contest, pk=self.kwargs.get('contest_id'))
        data = contest.scores.values('contestant__photo',
                                     'contestant__name',
                                     'contestant__org_name').annotate(
            score_sum=Sum('score')).order_by('-score_sum')

        host = self.request.get_host()
        for item in data:
            if item['contestant__photo']:
                item['contestant__photo'] = f'http://{host}{MEDIA_URL}{item["contestant__photo"]}'

        return data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = list(queryset)  # преобразуем QuerySet в список
        return JsonResponse({'results': results})
