from collections import OrderedDict

from django.contrib import admin, messages
from django.core.management import call_command
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from openpyxl.workbook import Workbook

from api.models import APIClient
from contests.models import Contest, Criteria, Stage, Track
from core.management.commands.add_scores import Command as AddScoresCommand
from core.management.commands.set_default import Command as SetDefaultScoresCommand
from core.utils import process_contest_data
from scores.models import Score
from users.models import Contestant, Judge


class MyAdmin(admin.ModelAdmin):
    """Переопределение общих параметров для всех моделей админки."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'

    class Meta:
        abstract = True


@admin.register(Contest)
class ContestAdmin(MyAdmin):
    """Регистрация модели конкурса в админке."""

    list_display = (
        'pk',
        'title',
        'description',
        'start_date',
        'end_date',
        'visible',
        'is_active',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    list_editable = ('visible', 'is_active',)
    search_fields = ('title', 'description', 'start_date',)
    list_filter = ('start_date', 'pub_date', 'update_date', 'visible', 'is_active',)
    actions = ['add_scores', 'set_default', 'save_results']

    @admin.action(description='Добавить оценки')
    def add_scores(self, request, queryset):
        for contest in queryset:
            message = call_command(AddScoresCommand(), contest_id=contest.pk)
            if message.startswith('Оценки добавлены'):
                self.message_user(request, message=message, level=messages.SUCCESS)
            else:
                self.message_user(request, message=message, level=messages.ERROR)

    @admin.action(description='Обнулить оценки')
    def set_default(self, request, queryset):
        for contest in queryset:
            message = call_command(SetDefaultScoresCommand(), contest_id=contest.pk)
            if message.startswith('Оценки обнулены'):
                self.message_user(request, message=message, level=messages.SUCCESS)
            else:
                self.message_user(request, message=message, level=messages.ERROR)

    @admin.action(description='Сохранить оценки в Excel')
    def save_results(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        header = ['Конкурс', 'Поток', 'Этап', 'Критерий', 'Судья', 'Команда', 'Оценка']
        ws.append(header)

        for contest in queryset:
            if not contest:
                return HttpResponse('Нет выбранных конкурсов.')
            scores = Score.objects.filter(contest=contest)
            for score in scores:
                row = [
                    score.contest.title,
                    score.track.title,
                    score.stage.title,
                    score.criteria.title,
                    score.judge.name,
                    score.contestant.name,
                    score.score,
                ]
                ws.append(row)

            ws.append([])  # Добавляем пустую строку

        # Создаем response и прикрепляем к нему excel файл
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=contest_scores.xlsx'
        wb.save(response)
        return response


@admin.register(Track)
class TrackAdmin(MyAdmin):
    """Регистрация модели потока в админке."""

    list_display = (
        'pk',
        'contest',
        'title',
        'description',
        'start_date',
        'end_date',
        'contestants_list',
        'judges_list',
        'order_index',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    list_editable = ('order_index',)
    search_fields = ('contest__title', 'title', 'description', 'start_date',)
    list_filter = ('start_date', 'pub_date', 'update_date',)


@admin.register(Stage)
class StageAdmin(MyAdmin):
    """Регистрация модели этапа в админке."""

    list_display = (
        'pk',
        'contest',
        'title',
        'description',
        'criterias_list',
        'questions_list',
        'type',
        'counting_method',
        'order_index',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    list_editable = ('order_index',)
    search_fields = ('contest__title', 'title', 'description',)
    list_filter = ('pub_date', 'update_date',)


@admin.register(Criteria)
class CriteriaAdmin(MyAdmin):
    """Регистрация модели критерия в админке."""

    list_display = (
        'pk',
        'title',
        'description',
        'min_score',
        'max_score',
        'order_index',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    list_editable = ('order_index',)
    search_fields = ('title',)
    list_filter = ('pub_date', 'update_date',)


@admin.register(Contestant)
class ContestantAdmin(MyAdmin):
    """Регистрация модели участника в админке."""

    list_display = (
        'pk',
        'full_name',
        'name',
        'org_name',
        'description',
        'photo',
        'participant_code',
        'ip_address',
        'order_index',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'name',)
    list_editable = ('order_index',)
    search_fields = ('name', 'org_name', 'description')
    list_filter = ('pub_date', 'update_date',)
    fields = ('name', 'org_name', 'description', 'photo', 'ip_address', 'get_html_photo',)
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')

    get_html_photo.short_description = 'Миниатюра'


@admin.register(Judge)
class JudgeAdmin(MyAdmin):
    """Регистрация модели судьи в админке."""

    list_display = (
        'pk',
        'full_name',
        'name',
        'org_name',
        'description',
        'photo',
        'slug',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'org_name', 'description')
    list_filter = ('pub_date', 'update_date',)
    fields = ('name', 'org_name', 'description', 'photo', 'slug', 'get_html_photo',)
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')

    get_html_photo.short_description = 'Миниатюра'


@admin.register(Score)
class ScoreAdmin(MyAdmin):
    """Регистрация модели оценки в админке."""

    list_display = (
        'pk',
        'judge',
        'contestant',
        'criteria',
        'question',
        'score',
        'contest',
        'track',
        'stage',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk',)
    list_editable = ('score',)
    search_fields = ('contest__title', 'track__title', 'stage__title',
                     'criteria__title', 'judge__name', 'contestant__name',)
    list_filter = ('pub_date', 'update_date', 'contest',)


@admin.register(APIClient)
class APIClientAdmin(MyAdmin):
    """Регистрация модели APIData в админке."""

    list_display = (
        'pk',
        'title',
        'link',
        'contest',
        'track',
        'stage',
    )
    list_display_links = ('pk', 'title',)
    readonly_fields = ('link',)
    actions = ['save_results']

    @admin.action(description='Сохранить оценки в Excel')
    def save_results(self, request, queryset):
        wb = Workbook()
        ws = wb.active

        # Получаем список названий всех этапов для всех клиентов в queryset
        stages = OrderedDict()
        for client in queryset:
            contest = client.contest
            for stage in contest.stages.all().order_by('order_index'):
                stages[stage.title] = None  # None здесь используется как placeholder

        # Формируем заголовок с названиями этапов и 'Итого'
        headers = ['Конкурс', 'Имя участника', 'Название организации'] + list(stages.keys()) + ['Итого']
        ws.append(headers)

        for client in queryset:
            contest = client.contest
            if not contest:
                continue
            track = client.track
            stage = client.stage
            results = process_contest_data(contest, track, stage)

            for result in results:
                # Создаем список с результатами этапов и итоговой суммой
                row_data = [
                               contest.title,
                               result['contestant__name'],
                               result['contestant__org_name']
                           ] + [
                               result['stages_scores'].get(stage_name, 0) for stage_name in stages
                           ] + [
                               result['score__sum_total']
                           ]

                # Добавляем данные в Excel
                ws.append(row_data)

            # Добавляем пустую строку для разделения конкурсов
            ws.append([])

        # Создаем response и прикрепляем к нему excel файл
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="contest_scores.xlsx"'

        # Сохраняем рабочую книгу в response
        wb.save(response)
        return response


admin.site.site_title = 'Poll Tracker'
admin.site.site_header = 'Poll Tracker Admin'
