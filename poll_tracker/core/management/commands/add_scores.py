from django.core.management.base import BaseCommand

from contests.models import Contest, Stage, Track
from scores.models import Score


class Command(BaseCommand):
    help = 'Создание дефолтных оценок для конкурса.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--contest-id',
            dest='contest_id',
            help='id конкурса для которого создаются оценки'
        )

    def handle(self, *args, **options):
        contest_id = options['contest_id']
        if contest_id:
            try:
                contest = Contest.objects.get(pk=contest_id)
            except Contest.DoesNotExist:
                message = f'Конкурс с id = {contest_id} не существует.'
                self.stdout.write(self.style.WARNING(message))
                return message
            tracks = Track.objects.filter(contest=contest).prefetch_related('contestants')
            if not tracks:
                message = f'Не созданы потоки для конкурса {contest.title}.'
                self.stdout.write(self.style.WARNING(message))
                return message
            stages = Stage.objects.filter(contest=contest).prefetch_related('criterias')
            if not stages:
                message = f'Не созданы этапы для конкурса {contest.title}.'
                self.stdout.write(self.style.WARNING(message))
                return message
            message = self.create_scores(contest, tracks, stages)
            return message
        else:
            message = 'Добавьте атрибут id-конкурса в вызов команды.'
            self.stdout.write(self.style.WARNING(message))
            return message

    def create_scores(self, contest, tracks, stages):
        for track in tracks:
            for stage in stages:
                if stage.type == 'judged':
                    for contestant in track.contestants.all():
                        for judge in track.judges.all():
                            for criteria in stage.criterias.all():
                                Score.objects.get_or_create(
                                    contest=contest,
                                    track=track,
                                    stage=stage,
                                    criteria=criteria,
                                    judge=judge,
                                    contestant=contestant,
                                )
                elif stage.type == 'brain_ring':
                    for contestant in track.contestants.all():
                        for question in stage.questions.all():
                            Score.objects.get_or_create(
                                contest=contest,
                                track=track,
                                stage=stage,
                                question=question,
                                judge=None,
                                contestant=contestant,
                            )

        message = f'Оценки добавлены для конкурса {contest.title}.'
        self.stdout.write(self.style.SUCCESS(message))
        return message
