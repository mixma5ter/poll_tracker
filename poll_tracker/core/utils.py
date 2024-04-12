from operator import itemgetter

from django.db.models import Sum

from scores.models import Score
from users.models import Contestant


def format_score(score):
    """Форматирует число, удаляя незначащие нули после запятой."""
    # Округление до двух знаков после запятой
    rounded_score = round(score, 2)
    # Преобразование в строку и удаление незначащих нулей
    return f"{rounded_score:.2f}".rstrip('0').rstrip('.')


def process_contest_data(contest, track=None, stage=None):
    # Если передан параметр track, фильтруем результаты по нему
    if track is not None:
        tracks = [track]
    else:
        tracks = contest.tracks.all().order_by('order_index')

    # Если передан параметр stage, фильтруем результаты по нему
    if stage is not None:
        stages = [stage]
    else:
        stages = contest.stages.all().order_by('order_index')

    data = []

    # Обходим все треки
    for track in tracks:
        judges_count = track.judges.count()

        # Если у потока нет судей, делить на ноль нельзя
        if judges_count == 0:
            continue  # Используем continue для перехода к следующему треку

        contestants = Contestant.objects.filter(tracks=track).distinct()

        # Обходим всех участников в треке
        for contestant in contestants:
            contestant_scores = Score.objects.filter(contestant=contestant, contest=contest)

            # Подготавливаем данные о сумме оценок для каждого этапа
            stages_scores = {}
            for stage in stages:
                stage_scores = contestant_scores.filter(stage=stage)
                score_sum = stage_scores.aggregate(Sum('score'))['score__sum'] or 0

                # Если метод подсчета 'avg', делим сумму на количество судей
                if stage.counting_method == 'avg' and judges_count > 0:
                    score_sum /= judges_count

                # Округляем до двух знаков и удаляем незначащие нули
                stages_scores[stage.title] = format_score(score_sum)

            # Подсчитываем общую сумму оценок для участников
            total_sum = sum(float(value) for value in stages_scores.values())

            # Добавляем результаты в список
            data.append({
                'contestant__photo': contestant.photo.url if contestant.photo else '',
                'contestant__name': contestant.name,
                'contestant__org_name': contestant.org_name,
                'score__sum_total': format_score(total_sum),
                'stages_scores': stages_scores,
            })

    # Сортируем результаты по общей сумме оценок, приведя строки к числам
    sorted_results = sorted(data, key=lambda x: float(x['score__sum_total']), reverse=True)

    return sorted_results
