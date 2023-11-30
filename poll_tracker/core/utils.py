from abc import ABC
from operator import itemgetter

from django.db.models import Avg, Sum, DecimalField, Func

ACCURACY = 2  # до скольки знаков после запятой округлять оценки


class Round(Func, ABC):
    function = 'ROUND'
    arity = 2
    output_field = DecimalField()


def process_contest_data(contest):
    """Получение результатов конкурса."""

    data_sum = contest.scores.filter(stage__counting_method='sum')
    data_avg = contest.scores.filter(stage__counting_method='avg')

    data_sum = data_sum.values(
        'contestant__name',
        'contestant__org_name'
    ).annotate(
        score__sum=Round(Sum('score'), ACCURACY, output_field=DecimalField())
    ).order_by()

    data_avg = data_avg.values(
        'contestant__name',
        'contestant__org_name'
    ).annotate(
        score__sum=Round(Avg('score'), ACCURACY, output_field=DecimalField())
    ).order_by()

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
