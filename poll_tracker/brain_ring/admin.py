from django.contrib import admin

from brain_ring.models import Question


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
    list_filter = ('is_active',)
