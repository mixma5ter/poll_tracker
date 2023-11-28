from operator import itemgetter

from django.db.models import Avg, DecimalField, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from contests.models import Contest
from core.utils import Round
from poll_tracker.settings import MEDIA_URL

ACCURACY = 2  # до скольки знаков после запятой округлять оценки


class ContestResultJson(viewsets.ModelViewSet):
    """Отправка данных в VMix."""

    def get_queryset(self):
        contest = get_object_or_404(Contest, pk=self.kwargs.get('contest_id'))

        data_sum = contest.scores.filter(stage__counting_method='sum')
        data_avg = contest.scores.filter(stage__counting_method='avg')

        data_sum = data_sum.values(
            'contestant__photo',
            'contestant__name',
            'contestant__org_name'
        ).annotate(
            score_sum=Round(Sum('score'), ACCURACY, output_field=DecimalField())
        ).order_by()

        data_avg = data_avg.values(
            'contestant__photo',
            'contestant__name',
            'contestant__org_name'
        ).annotate(
            score_sum=Round(Avg('score'), ACCURACY, output_field=DecimalField())
        ).order_by()

        data_combined = [*data_sum, *data_avg]

        host = self.request.get_host()
        for item in data_combined:
            item['contestant__full_name'] = f'{item["contestant__name"]} - {item["contestant__org_name"]}'
            if item['contestant__photo']:
                item['contestant__photo'] = f'http://{host}{MEDIA_URL}{item["contestant__photo"]}'

        return data_combined

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        merged_results = {}

        for result in results:
            contestant_name = result['contestant__name']
            if contestant_name not in merged_results:
                merged_results[contestant_name] = result
            else:
                merged_results[contestant_name]['score_sum'] += result['score_sum']

        sorted_results = sorted(merged_results.values(), key=itemgetter('score_sum'), reverse=True)

        return JsonResponse({'results': sorted_results})
