from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from core.models import CreatedModel


class Score(CreatedModel):
    """Модель оценки."""

    id = models.BigAutoField(
        primary_key=True
    )
    contest = models.ForeignKey(
        'contests.Contest',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='scores',
        verbose_name='Конкурс',
        help_text='Выберите конкурс',
    )
    track = ChainedForeignKey(
        'contests.Track',
        db_index=True,
        chained_field='contest',
        chained_model_field='contest',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        verbose_name='Поток',
        help_text='Выберите поток',
    )
    stage = ChainedForeignKey(
        'contests.Stage',
        db_index=True,
        chained_field='contest',
        chained_model_field='contest',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        verbose_name='Этап',
        help_text='Выберите этап',
    )
    criteria = ChainedForeignKey(
        'contests.Criteria',
        db_index=True,
        blank=True,
        null=True,
        chained_field='stage',
        chained_model_field='stages',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        verbose_name='Критерий',
        help_text='Выберите критерий',
    )
    question = ChainedForeignKey(
        'brain_ring.Question',
        db_index=True,
        blank=True,
        null=True,
        chained_field='stage',
        chained_model_field='stages',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        help_text='Выберите вопрос',
    )
    judge = ChainedForeignKey(
        'users.Judge',
        db_index=True,
        blank=True,
        null=True,
        chained_field='track',
        chained_model_field='tracks',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        verbose_name='Судья',
        help_text='Выберите судью',
    )
    contestant = ChainedForeignKey(
        'users.Contestant',
        db_index=True,
        chained_field='track',
        chained_model_field='tracks',
        show_all=False,
        auto_choose=True,
        on_delete=models.CASCADE,
        verbose_name='Команда',
        help_text='Выберите команду',
    )
    score = models.SmallIntegerField(
        default=0,
        db_index=True,
        verbose_name='Оценка',
        help_text='Выберите оценку',
    )

    def __str__(self):
        return '{} поставил оценку {} за {} команде {}'.format(
            self.judge,
            self.score,
            self.criteria,
            self.contestant
        )

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['contest', 'track', 'stage', 'criteria', 'judge', 'contestant'],
                name='unique_score_model'
            )
        ]
