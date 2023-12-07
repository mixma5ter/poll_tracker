from operator import itemgetter

from django.db.models import Sum

from scores.models import Score


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
