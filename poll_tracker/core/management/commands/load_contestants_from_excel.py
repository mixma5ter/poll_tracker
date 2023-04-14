import openpyxl

from django.core.management import BaseCommand
from users.models import Contestant


class Command(BaseCommand):
    help = 'Загрузка участников в БД из таблицы Excel'

    def handle(self, *args, **options):
        workbook = openpyxl.load_workbook('data/contestants.xlsx')
        worksheet = workbook.active

        uploaded = 0
        not_loaded = 0

        for row in worksheet:
            try:
                Contestant.objects.get_or_create(
                    org_name=row[0].value,  # имя организации (колонка 1)
                    name=row[1].value,  # имя команды (колонка 2)
                )
                uploaded += 1
            except ValueError:
                print(f'Ошибка загрузки - {row[0].value}')
                not_loaded += 1

        message = f'\nЗагружено - {uploaded}. Ошибок - {not_loaded}'

        self.stdout.write(self.style.SUCCESS(message))
