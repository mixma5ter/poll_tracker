import sys

from django.core.management.base import BaseCommand

from contests.models import Contest, Criteria, Stage, Track
from scores.models import Score
from users.models import Contestant, Judge


class Command(BaseCommand):
    help = 'Создание дефолтных оценок для конкурса.'

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
        except Exception as exc:
            message = f'Конкурс с id = {contest_id} не существует - {exc}.'
            self.stdout.write(self.style.WARNING(message))
            sys.exit()

        tracks = contest.tracks.all()
        if not tracks:
            message = f'Не созданы потоки для конкурса {contest.title}.'
            self.stdout.write(self.style.WARNING(message))
            sys.exit()

        stages = contest.stages.all()
        if not stages:
            message = f'Не созданы этапы для конкурса {contest.title}.'
            self.stdout.write(self.style.WARNING(message))
            sys.exit()

        contestants = Contestant.objects.filter(tracks__in=tracks)
        judges = Judge.objects.filter(tracks__in=tracks)
        criterias = Criteria.objects.filter(stages__in=stages)

        for track in tracks:
            for contestant in contestants:
                for judge in judges:
                    for stage in stages:
                        for criteria in criterias:
                            Score.objects.get_or_create(
                                contest=contest,
                                track=track,
                                stage=stage,
                                criteria=criteria,
                                judge=judge,
                                contestant=contestant,
                            )

        message = f'\nОценки загружены'

        self.stdout.write(self.style.SUCCESS(message))
