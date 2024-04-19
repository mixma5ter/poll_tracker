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

        data_with_photos = []
        for item in results:
            # Дополнительно обогащаем данные URL фотографий
            if item.get('contestant__photo'):
                item['contestant__photo'] = f'http://{host}{MEDIA_URL}{item["contestant__photo"]}'

            # Добавляем данные конкурса (при наличии)
            item['contest__title'] = contest.title
            item['contest__track'] = track.title if track else ""
            item['contest__stage'] = stage.title if stage else ""
            item['contest__stage'] = stage.title if stage else "Итог"

            # Можно добавить дополнительную информацию в item, если это необходимо
            data_with_photos.append(item)

        return data_with_photos

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        if results:
            return JsonResponse({'results': results})
        else:
            # Вы можете отправить пустой результат или сообщение об ошибке
            return JsonResponse({'message': 'No results found'}, status=404)
