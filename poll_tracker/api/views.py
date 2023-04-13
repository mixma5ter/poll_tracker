from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from contests.models import Contest


class ContestResultJson(viewsets.ModelViewSet):
    """Модель отправки данных в VMix."""

    def get_queryset(self):
        contest = get_object_or_404(Contest, pk=self.kwargs.get('contest_id'))
        data = contest.scores.values('contestant__name', 'contestant__org_name').annotate(
            Sum('score')).order_by('contestant')
        ordered_data = data.order_by('-score__sum')
        return ordered_data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = list(queryset)  # преобразуем QuerySet в список
        return JsonResponse({'results': results})
