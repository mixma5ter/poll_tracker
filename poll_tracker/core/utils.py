from operator import itemgetter

from django.db.models import Sum

from scores.models import Score
from users.models import Contestant


def process_contest_data(contest, track=None, stage=None):
    scores = Score.objects.filter(contest=contest)
    if track:
        scores = scores.filter(track=track)
    if stage:
        scores = scores.filter(stage=stage)

    tracks = contest.tracks.all().order_by('order_index')

    scores_sum = scores.filter(stage__counting_method='sum')
    scores_avg = scores.filter(stage__counting_method='avg')

    data_sum = []
    data_avg = []

    for track in tracks:
        judges_count = len(track.judges.all())

        # Если у потока нет судей, делить на ноль нельзя
        if judges_count == 0:
            return None
        # Сумма оценок потока
        data_sum += scores_sum.filter(track=track).values(
            'contestant__photo',
            'contestant__name',
            'contestant__org_name'
        ).annotate(
            score__sum=Sum('score')
        ).order_by('-score__sum')

        # Сумма оценок деленная на количество судей потока
        data_avg += scores_avg.filter(track=track).values(
            'contestant__photo',
            'contestant__name',
            'contestant__org_name'
        ).annotate(
            score__sum=Sum('score')/judges_count
        ).order_by('-score__sum')

    data_combined = [*data_sum, *data_avg]

    merged_results = {}

    for result in data_combined:
        contestant_name = result['contestant__name']
        if contestant_name not in merged_results:
            merged_results[contestant_name] = result
        else:
            merged_results[contestant_name]['score__sum'] += result['score__sum']

    sorted_results = sorted(merged_results.values(), key=itemgetter('score__sum'), reverse=True)

    return sorted_results


def process_contest_data_with_stages(contest, track=None, stage=None):
    scores = Score.objects.filter(contest=contest)

    tracks = contest.tracks.all().order_by('order_index')

    data = []

    # Обходим все треки
    for track in tracks:
        judges_count = track.judges.count()

        # Если у потока нет судей, делить на ноль нельзя
        if judges_count == 0:
            return None

        contestants = Contestant.objects.filter(tracks=track).distinct()

        # Обходим всех участников в треке
        for contestant in contestants:
            contestant_scores = scores.filter(contestant=contestant)

            # Подготавливаем данные о сумме оценок для каждого этапа
            stages_scores = {}
            for stage in contest.stages.all().order_by('order_index'):
                stage_scores = contestant_scores.filter(stage=stage)
                stages_scores[stage.title] = stage_scores.aggregate(
                    Sum('score')
                )['score__sum'] or 0

                # Если метод подсчета 'avg', делим сумму на количество судей
                if stage.counting_method == 'avg':
                    stages_scores[stage.title] /= judges_count

            # Подсчитываем общую сумму оценок для участников
            total_sum = sum(stages_scores.values())

            # Добавляем результаты в список
            data.append({
                'contestant__photo': contestant.photo.url if contestant.photo else '',
                'contestant__name': contestant.name,
                'contestant__org_name': contestant.org_name,
                'score__sum_total': total_sum,
                'stages_scores': stages_scores,
            })

    # Сортируем результаты по общей сумме оценок
    sorted_results = sorted(data, key=itemgetter('score__sum_total'), reverse=True)

    return sorted_results
