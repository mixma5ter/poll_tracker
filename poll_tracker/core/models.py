from django.db import models


class CreatedModel(models.Model):
    """Общие поля для всех моделей проекта."""

    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        abstract = True
