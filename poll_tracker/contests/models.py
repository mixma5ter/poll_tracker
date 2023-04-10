from django.db import models
from django.urls import reverse

from core.models import CreatedModel


class Contest(CreatedModel):
    """Модель конкурса."""

    id = models.BigAutoField(
        primary_key=True
    )
    title = models.CharField(
        max_length=255,
        unique_for_date='pub_date',
        verbose_name='Конкурс',
        help_text='Введите название конкурса',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание конкурса',
    )
    start_date = models.DateField(
        verbose_name='Дата начала',
        help_text='Выберите дату начала конкурса',
    )
    end_date = models.DateField(
        verbose_name='Дата окончания',
        help_text='Выберите дату окончания конкурса',
    )
    visible = models.BooleanField(
        default=False,
        verbose_name='Видимость конкурса',
        help_text='Установите флажок для отображения конкурса на сайте',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Идет голосование',
        help_text='Установите флажок перед началом голосования, снимите после завершения',
    )

    # def get_absolute_url(self):
    #     return reverse('contest', kwargs={'contest_pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'
        ordering = ('-start_date', 'pub_date', 'title',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'start_date'],
                name='unique_contest_model'
            )
        ]


class Track(CreatedModel):
    """Модель потока конкурса."""

    id = models.BigAutoField(
        primary_key=True
    )
    contest = models.ForeignKey(
        'Contest',
        on_delete=models.CASCADE,
        related_name='tracks',
        verbose_name='Конкурс',
        help_text='Выберите конкурс',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название потока',
        help_text='Введите название потока',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание потока',
    )
    contestants = models.ManyToManyField(
        'users.Contestant',
        related_name='tracks',
        verbose_name='Участники',
        help_text='Выберите участников.',
    )
    judges = models.ManyToManyField(
        'users.Judge',
        default='Отсутствует',
        related_name='tracks',
        verbose_name='Судьи',
        help_text='Выберите судей.',
    )
    start_date = models.DateField(
        verbose_name='Дата начала',
        help_text='Выберите дату начала потока',
    )
    end_date = models.DateField(
        verbose_name='Дата окончания',
        help_text='Выберите дату окончания потока',
    )

    def contestants_list(self):
        return '{}'.format(', '.join([contestant.name for contestant in self.contestants.all()]))

    contestants_list.short_description = 'Участники'

    def judges_list(self):
        return '{}'.format(', '.join([judge.name for judge in self.judges.all()]))

    judges_list.short_description = 'Судьи'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поток конкурса'
        verbose_name_plural = 'Потоки конкурса'
        ordering = ('-start_date', 'pub_date', 'title',)
        constraints = [
            models.UniqueConstraint(
                fields=['contest', 'title'],
                name='unique_track_model'
            )
        ]


class Stage(CreatedModel):
    """Модель этапа конкурса."""

    id = models.BigAutoField(
        primary_key=True
    )
    contest = models.ForeignKey(
        'Contest',
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name='Конкурс',
        help_text='Выберите конкурс',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название этапа конкурса',
        help_text='Введите название этапа конкурса',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание этапа конкурса',
    )
    criterias = models.ManyToManyField(
        'Criteria',
        related_name='stages',
        verbose_name='Критерии',
        help_text='Выберите критерии этапа конкурса.',
    )
    is_judged = models.BooleanField(
        default=True,
        verbose_name='Оценивается судьями',
        help_text='Установите флажок если этап оценивается судьями',
    )

    def criterias_list(self):
        return '{}'.format(', '.join([criteria.title for criteria in self.criterias.all()]))

    criterias_list.short_description = 'Критерии'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Этап конкурса'
        verbose_name_plural = 'Этапы конкурса'
        ordering = ('contest', 'title', 'pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['contest', 'title'],
                name='unique_stage_model'
            )
        ]


class Criteria(CreatedModel):
    """Модель критерия этапа конкурса."""

    id = models.BigAutoField(
        primary_key=True
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название критерия',
        help_text='Введите название критерия конкурса',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание критерия этапа конкурса',
    )
    min_score = models.SmallIntegerField(
        default=0,
        verbose_name='Минимальная оценка',
        help_text='Минимальная оценка критерия',
    )
    max_score = models.SmallIntegerField(
        default=10,
        verbose_name='Максимальная оценка',
        help_text='Максимальная оценка критерия',
    )

    def score_choices(self):
        """Генерируем выпадающий список для формы оценки."""
        return [(i, str(i)) for i in range(self.min_score, self.max_score + 1)]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Критерий конкурса'
        verbose_name_plural = 'Критерии конкурса'
        ordering = ('title',)
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_criteria_model'
            )
        ]
