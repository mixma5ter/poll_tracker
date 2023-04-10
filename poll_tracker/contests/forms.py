from django import forms

from scores.models import Score


class ScoreForm(forms.ModelForm):
    """Форма оценки."""

    class Meta:
        model = Score
        fields = ['criteria', 'score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        criteria = self.instance.criteria
        self.fields['score'].choices = criteria.score_choices()
