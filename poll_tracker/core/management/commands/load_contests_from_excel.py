import openpyxl

from django.core.management import BaseCommand
from contests.models import Contest


class Command(BaseCommand):
    help = 'Загрузка конкурсов в БД из таблицы Excel'

    def handle(self, *args, **options):
        workbook = openpyxl.load_workbook('data/contests.xlsx')
        worksheet = workbook.active

        uploaded = 0
        not_loaded = 0

        for row in worksheet:
            # print(row[0].value, row[1].value, end='\n')
            try:
                Contest.objects.get_or_create(
                    title=row[0].value,  # название конкурса (колонка 1)
                    description=row[1].value,  # описание конкурса (колонка 2)
                    start_date=row[2].value,  # дата начала (колонка 3)
                    end_date=row[3].value,  # дата окончания (колонка 4)
                )
                uploaded += 1
            except ValueError:
                print(f'Ошибка загрузки - {row[0].value}')
                not_loaded += 1

        message = f'\nЗагружено - {uploaded}. Ошибок - {not_loaded}'

        self.stdout.write(self.style.SUCCESS(message))
