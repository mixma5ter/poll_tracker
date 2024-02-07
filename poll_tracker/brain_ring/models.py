from django.db import models


class Question(models.Model):
    """Модель вопроса."""

    question_index = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Индекс вопроса',
        help_text='Введите порядковый номер вопроса в этапе',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активный вопрос',
        help_text='Определите, является ли вопрос активным',
    )
    text = models.TextField(
        verbose_name='Текст вопроса',
        help_text='Введите текст вопроса',
    )
    options = models.TextField(
        verbose_name='Варианты ответа',
        help_text='Введите варианты ответа через точку с запятой (;)',
    )
    correct_answer = models.CharField(
        max_length=255,
        verbose_name='Правильный ответ',
        help_text='Введите правильный ответ',
    )
    points = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Баллы за правильный ответ',
        help_text='Введите количество баллов за правильный ответ',
    )

    def __str__(self):
        return f'Вопрос {self.question_index}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('question_index',)
