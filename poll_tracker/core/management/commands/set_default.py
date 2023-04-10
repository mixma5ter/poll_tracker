import sys

from django.core.management.base import BaseCommand

from contests.models import Contest, Criteria, Stage, Track
from scores.models import Score
from users.models import Contestant, Judge


class Command(BaseCommand):
    help = 'Сброс всех оценок конкурса.'

    def add_arguments(self, parser):
        parser.add_argument(
            'contest_id',
            type=int,
            help='id конкурса для которого создаются оценки'
        )

    def handle(self, *args, **options):

        contest_id = options['contest_id']
        try:
            contest = Contest.objects.get(pk=contest_id)
        except Contest.DoesNotExist:
            message = f'Конкурс с id = {contest_id} не существует.'
            self.stdout.write(self.style.WARNING(message))
            sys.exit()

        tracks = Track.objects.filter(contest=contest).prefetch_related('contestants')
        if not tracks:
            message = f'Не созданы потоки для конкурса {contest.title}.'
            self.stdout.write(self.style.WARNING(message))
            sys.exit()

        stages = Stage.objects.filter(contest=contest).prefetch_related('criterias')
        if not stages:
            message = f'Не созданы этапы для конкурса {contest.title}.'
            self.stdout.write(self.style.WARNING(message))
            sys.exit()

        contestants = Contestant.objects.filter(tracks__in=tracks)
        judges = Judge.objects.filter(tracks__in=tracks)

        # criterias = Criteria.objects.filter(stages__in=stages)
        criterias = Criteria.objects.filter(stages__in=stages).select_related()

        scores = Score.objects.filter(contest=contest)
        for score in scores:
            if score.score != score.criteria.min_score:
                score.score = score.criteria.min_score
                score.save()

        message = f'\nОценки обнулены'

        self.stdout.write(self.style.SUCCESS(message))
