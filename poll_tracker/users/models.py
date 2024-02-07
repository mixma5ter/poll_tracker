import uuid

from django.db import models

from core.models import CreatedModel


class Contestant(CreatedModel):
    """Модель участника конкурса."""

    id = models.BigAutoField(
        primary_key=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Команда',
        help_text='Введите название',
    )
    org_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Организация',
        help_text='Введите организацию',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание',
    )
    photo = models.ImageField(
        blank=True,
        upload_to='contestants',
        verbose_name='Логотип',
        help_text='Добавьте логотип',
    )
    participant_code = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name='Шифр',
    )
    ip_address = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='IP-адрес',
    )
    order_index = models.SmallIntegerField(
        default=1,
        verbose_name='Индекс',
        help_text='Порядковый индекс',
    )

    def full_name(self):
        return '{}'.format(' - '.join(str(item) for item in [self.name, self.org_name] if item))

    full_name.short_description = 'Команда - Организация'

    def __str__(self):
        return self.full_name()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'org_name'],
                name='unique_contestant_model'
            )
        ]


class Judge(CreatedModel):
    """Модель судьи конкурса."""

    id = models.BigAutoField(
        primary_key=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='ФИО',
        help_text='Введите ФИО',
    )
    slug = models.SlugField(
        max_length=255,
        auto_created=True,
        verbose_name='Слаг',
    )
    org_name = models.CharField(
        blank=True,
        max_length=255,
        verbose_name='Организация',
        help_text='Введите название организации',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Введите описание',
    )
    photo = models.ImageField(
        blank=True,
        upload_to='contestants',
        verbose_name='Фотография',
        help_text='Добавьте фотографию',
    )

    def full_name(self):
        return '{}'.format(' - '.join(str(item) for item in [self.name, self.org_name] if item))

    full_name.short_description = 'ФИО - Организация'

    def __str__(self):
        return self.full_name()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'org_name', 'slug'],
                name='unique_judge_model'
            )
        ]
