from django import forms

from scores.models import Score


class ScoreForm(forms.ModelForm):
    """Форма оценки."""

    class Meta:
        model = Score
        fields = ['criteria', 'score']
