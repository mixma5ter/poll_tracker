from django.db import models

from contests.models import Stage


class Question(models.Model):
    """Модель вопроса."""

    CORRECT_ANSWER_CHOICES = [
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
        (4, 'D'),
    ]

    stage = models.ForeignKey(
        Stage,
        limit_choices_to={'type': 'brain_ring'},
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Этап',
        help_text='Выберите этап',
    )
    question_index = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Индекс вопроса',
        help_text='Введите порядковый номер вопроса в этапе',
    )
    correct_answer = models.PositiveSmallIntegerField(
        default=1,
        choices=CORRECT_ANSWER_CHOICES,
        verbose_name='Правильный ответ',
        help_text='Выберите правильный ответ',
    )

    def __str__(self):
        return f'Вопрос {self.question_index}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('stage', 'question_index',)
        constraints = [
            models.UniqueConstraint(
                fields=['stage', 'question_index'],
                name='unique_question_model'
            )
        ]
