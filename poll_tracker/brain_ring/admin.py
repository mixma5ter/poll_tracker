from django.contrib import admin

from brain_ring.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Регистрация модели вопросов в админке."""

    list_display = (
        'stage',
        'question_index',
        'is_active',
        'text',
        'options',
        'correct_answer',
    )
    list_editable = ('question_index', 'is_active',)
    search_fields = ('stage', 'question_index',)
    list_filter = ('stage', 'is_active',)
