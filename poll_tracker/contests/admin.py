from django.contrib import admin
from django.utils.safestring import mark_safe

from contests.models import Contest, Criteria, Stage, Track
from scores.models import Score
from users.models import Contestant, Judge


class MyAdmin(admin.ModelAdmin):
    """Переопределение общих параметров для всех моделей админки."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'

    class Meta:
        abstract = True


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
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    search_fields = ('contest__title', 'title', 'description', 'start_date',)
    list_filter = ('start_date', 'pub_date', 'update_date',)


class StageAdmin(MyAdmin):
    """Регистрация модели этапа в админке."""

    list_display = (
        'pk',
        'contest',
        'title',
        'description',
        'criterias_list',
        'is_judged',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    search_fields = ('contest__title', 'title', 'description',)
    list_filter = ('pub_date', 'update_date',)


class CriteriaAdmin(MyAdmin):
    """Регистрация модели критерия в админке."""

    list_display = (
        'pk',
        'title',
        'description',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'title',)
    search_fields = ('title',)
    list_filter = ('pub_date', 'update_date',)


class ContestantAdmin(MyAdmin):
    """Регистрация модели участника в админке."""

    list_display = (
        'pk',
        'full_name',
        'name',
        'org_name',
        'description',
        'photo',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'name',)
    search_fields = ('name', 'org_name', 'description')
    list_filter = ('pub_date', 'update_date',)
    fields = ('name', 'org_name', 'description', 'photo', 'get_html_photo',)
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')
    get_html_photo.short_description = 'Миниатюра'


class JudgeAdmin(MyAdmin):
    """Регистрация модели судьи в админке."""

    list_display = (
        'pk',
        'full_name',
        'name',
        'org_name',
        'description',
        'photo',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk', 'name',)
    search_fields = ('name', 'org_name', 'description')
    list_filter = ('pub_date', 'update_date',)
    fields = ('name', 'org_name', 'description', 'photo', 'get_html_photo',)
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50')

    get_html_photo.short_description = 'Миниатюра'


class ScoreAdmin(MyAdmin):
    """Регистрация модели оценки в админке."""

    list_display = (
        'pk',
        'contest',
        'track',
        'stage',
        'criteria',
        'judge',
        'contestant',
        'score',
        'pub_date',
        'update_date',
    )
    list_display_links = ('pk',)
    list_editable = ('score',)
    search_fields = ('contest__title', 'track__title', 'stage__title',
                     'criteria__title', 'judge__name', 'contestant__name',)
    list_filter = ('pub_date', 'update_date',)


admin.site.register(Contest, ContestAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Contestant, ContestantAdmin)
admin.site.register(Judge, JudgeAdmin)
admin.site.register(Score, ScoreAdmin)

admin.site.site_title = 'Poll Tracker'
admin.site.site_header = 'Poll Tracker Admin'
