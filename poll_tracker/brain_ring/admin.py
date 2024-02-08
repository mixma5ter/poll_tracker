from django.contrib import admin

from contests.models import Stage
from brain_ring.models import Question


class QuestionStageInline(admin.TabularInline):
    """Промежуточная модель связи между вопросами и этапами.

    Модель используется для добавления фильтрации по названию этапа в админке."""

    model = Stage.questions.through
    extra = 0
    verbose_name = 'Этап'
    verbose_name_plural = 'Этапы'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Регистрация модели вопросов в админке."""

    list_display = (
        'pk',
        'question_index',
        'is_active',
        'text',
        'options',
        'correct_answer',
        'points',
    )
    list_editable = ('question_index', 'is_active', 'points',)
    search_fields = ('question_index',)
    inlines = [QuestionStageInline]
    list_filter = ('stages__title',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('stages')
        return queryset
