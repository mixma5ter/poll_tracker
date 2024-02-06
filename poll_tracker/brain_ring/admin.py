from django.contrib import admin

from brain_ring.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Регистрация модели вопросов в админке."""

    list_display = (
        'stage',
        'question_index',
        'correct_answer',
    )
    list_editable = ('question_index', 'correct_answer',)
    search_fields = ('stage', 'question_index',)
    list_filter = ('stage',)
