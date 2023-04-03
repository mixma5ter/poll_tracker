import openpyxl

from django.core.management import BaseCommand
from users.models import Judge


class Command(BaseCommand):
    help = 'Загрузка судей в БД из таблицы Excel'

    def handle(self, *args, **options):
        workbook = openpyxl.load_workbook('data/judges.xlsx')
        worksheet = workbook.active

        uploaded = 0
        not_loaded = 0

        for row in worksheet:
            # print(row[0].value, row[1].value, end='\n')
            try:
                Judge.objects.get_or_create(
                    name=row[0].value,  # имя судьи (колонка 1)
                    description=row[1].value,  # описание (колонка 2)
                )
                uploaded += 1
            except ValueError:
                print(f'Ошибка загрузки - {row[0].value}')
                not_loaded += 1

        message = f'\nЗагружено - {uploaded}. Ошибок - {not_loaded}'

        self.stdout.write(self.style.SUCCESS(message))
