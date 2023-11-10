from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from contests.models import Contest


class ContestResultJson(viewsets.ModelViewSet):
    """Отправка данных в VMix."""

    def get_queryset(self):
        request = self.request
        contest = get_object_or_404(Contest, pk=self.kwargs.get('contest_id'))
        data = contest.scores.values('contestant__photo',
                                     'contestant__name',
                                     'contestant__org_name').annotate(
            Sum('score')).order_by('contestant')

        # Перебираем данные и создаем абсолютный URL для каждой фотографии
        for item in data:
            item['contestant__photo'] = request.build_absolute_uri(item['contestant__photo'])

        ordered_data = data.order_by('-score__sum')
        return ordered_data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = list(queryset)  # преобразуем QuerySet в список
        return JsonResponse({'results': results})
