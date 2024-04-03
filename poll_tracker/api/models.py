from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from poll_tracker.settings import ALLOWED_HOSTS, PORT


class APIClient(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Клиент',
        help_text='Введите название клиента'
    )
    link = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Ссылка на API',
    )
    contest = models.ForeignKey(
        'contests.Contest',
        db_index=True,
        related_name='contest',
        on_delete=models.SET_NULL,  # NULL при удалении связанного объекта
        null=True,
        blank=True,
        verbose_name='Конкурс',
        help_text='Выберите конкурс'
    )
    track = ChainedForeignKey(
        'contests.Track',
        db_index=True,
        chained_field='contest',
        chained_model_field='contest',
        on_delete=models.SET_NULL,  # NULL при удалении связанного объекта
        null=True,
        blank=True,
        verbose_name='Поток',
        help_text='Выберите поток'
    )
    stage = ChainedForeignKey(
        'contests.Stage',
        db_index=True,
        chained_field='contest',
        chained_model_field='contest',
        on_delete=models.SET_NULL,  # NULL при удалении связанного объекта
        null=True,
        blank=True,
        verbose_name='Этап',
        help_text='Выберите этап'
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Проверяем, что объект является новым
            # Генерируем ссылку на API на основе имени нового объекта
            host = ALLOWED_HOSTS[0]
            port = PORT
            self.link = f'http://{host}:{port}/api/{self.title}/'
        super(APIClient, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'API клиент'
        verbose_name_plural = 'API клиенты'
        ordering = ('pk',)
