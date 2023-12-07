from operator import itemgetter

from django.db.models import Sum, Count, FloatField

from scores.models import Score


def process_contest_data(contest):
    """Получение результатов конкурса."""

    tracks = contest.tracks.all().order_by('order_index')

    scores_sum = contest.scores.filter(stage__counting_method='sum')
    scores_avg = contest.scores.filter(stage__counting_method='avg')

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


def process_stage_data(stage):
    """Получение результатов этапа конкурса."""
    scores = Score.objects.filter(stage=stage)  # Фильтруем оценки по текущему этапу
    data = []

    if stage.counting_method == 'sum':
        data = scores.values(
            'contestant__photo',
            'contestant__name',
            'contestant__org_name'
        ).annotate(
            score__sum=Sum('score')
        ).order_by('-score__sum')
    elif stage.counting_method == 'avg':
        data = scores.values(
            'contestant__photo',
            'contestant__name',
            'contestant__org_name'
        ).annotate(
            judges_count=Count('judge', distinct=True),
            score__sum=Sum('score') / Count('judge', distinct=True, output_field=FloatField())
        ).order_by('-score__sum')

    return data
