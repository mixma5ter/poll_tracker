from django.core.management.base import BaseCommand

from contests.models import Contest, Criteria, Stage
from scores.models import Score


class Command(BaseCommand):
    help = 'Сброс всех оценок конкурса.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--contest-id',
            dest='contest_id',
            help='id конкурса для которого сбрасываются оценки'
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
            if contest.is_active:
                message = f'Конкурс {contest.title} активен. Невозможно обнулить оценки по активному конкурсу'
                self.stdout.write(self.style.WARNING(message))
                return message
            stages = Stage.objects.filter(contest=contest).prefetch_related('criterias')
            if not stages:
                message = f'Не созданы этапы для конкурса {contest.title}.'
                self.stdout.write(self.style.WARNING(message))
                return message
            criterias = Criteria.objects.filter(stages__in=stages).select_related()
            if not criterias:
                message = f'Не созданы критерии конкурса {contest.title}.'
                self.stdout.write(self.style.WARNING(message))
                return message
            message = self.set_default(contest, criterias)
            return message
        else:
            message = 'Добавьте атрибут id-конкурса в вызов команды.'
            return message

    def set_default(self, contest, criterias):
        scores = Score.objects.filter(contest=contest)
        for score in scores:
            if score.score != score.criteria.min_score:
                score.score = score.criteria.min_score
                score.save()

        message = f'Оценки обнулены для конкурса {contest.title}'
        self.stdout.write(self.style.SUCCESS(message))
        return message
