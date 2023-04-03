import openpyxl

from django.core.management import BaseCommand
from contests.models import Criteria


class Command(BaseCommand):
    help = 'Загрузка критериев в БД из таблицы Excel'

    def handle(self, *args, **options):
        workbook = openpyxl.load_workbook('data/criterias.xlsx')
        worksheet = workbook.active

        uploaded = 0
        not_loaded = 0

        for row in worksheet:
            # print(row[0].value, row[1].value, end='\n')
            try:
                Criteria.objects.get_or_create(
                    title=row[0].value,  # название критекия (колонка 1)
                )
                uploaded += 1
            except ValueError:
                print(f'Ошибка загрузки - {row[0].value}')
                not_loaded += 1

        message = f'\nЗагружено - {uploaded}. Ошибок - {not_loaded}'

        self.stdout.write(self.style.SUCCESS(message))
