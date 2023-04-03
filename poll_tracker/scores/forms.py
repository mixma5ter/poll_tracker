from django import forms

from contests.models import Contest, Criteria, Stage, Track
from users.models import Contestant, Judge
from .models import Score


class AddScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['contest', 'track', 'stage', 'criteria', 'judge', 'contestant', 'score']

    contest = Contest.objects.all()
    track = Track.objects.all()
    stage = Stage.objects.all()
    criteria = Criteria.objects.all()
    judge = Judge.objects.all()
    contestant = Contestant.objects.all()
