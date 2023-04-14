import django_tables2 as tables
from .models import Score


class ResultTable(tables.Table):
    """Таблица результатов конкурса."""

    class Meta:
        model = Score
        template_name = 'django_tables2/bootstrap.html'
        fields = ('contestant__name', 'contestant__org_name', 'score__sum',)
