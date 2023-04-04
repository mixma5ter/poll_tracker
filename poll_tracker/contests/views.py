from django.forms import modelformset_factory
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from contests.models import Contest, Stage, Track
from scores.models import Score


class ContestsListView(ListView):
    """Страница со списком конкурсов."""

    model = Contest
    template_name = 'contests/contest_list.html'
    context_object_name = 'contests'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Конкурсы'
        return context

    def get_queryset(self):
        return Contest.objects.filter(visible=True).order_by('-start_date')


class ContestDetailView(DetailView):
    """Страница конкурса с описанием."""

    model = Contest
    template_name = 'contests/contest_detail.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Описание конкурса'
        context['tracks'] = Track.objects.filter(contest=self.get_object()).order_by('pub_date')
        return context


class ContestStageView(DetailView):
    """Страница выбора этапа конкурса."""

    model = Contest
    template_name = 'contests/contest_stage.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        track_id = self.kwargs['track_pk']
        track = Track.objects.get(pk=track_id)
        context['title'] = 'Этапы конкурса'
        context['track'] = track
        context['stages'] = Stage.objects.filter(contest=self.get_object())
        return context


def add_score_view(request, contest_pk: int, track_pk: int, stage_pk: int):
    """Страница голосования."""

    template_name = 'contests/contest_polling.html'

    contest = Contest.objects.get(pk=contest_pk)
    track = Track.objects.get(pk=track_pk)
    stage = Stage.objects.get(pk=stage_pk)

    ScoreFormset = modelformset_factory(
        Score,
        fields=('score',),
        extra=0
    )

    if request.method in ('POST', 'PUT'):
        formset = ScoreFormset(
            request.POST,
            queryset=Score.objects.filter(
                contest__pk=contest.id
            ).filter(
                track__pk=track.id
            ).filter(
                stage__pk=stage.id
            )
        )

        if formset.is_valid():
            instances = formset.save()
            for instance in instances:
                instance.contest_id = contest.id
                instance.track_id = track.id
                instance.stage_id = stage.id
                instance.save()

    formset = ScoreFormset(
        queryset=Score.objects.filter(contest__id=contest.id)
    )
    context = {
        'formset': formset
    }
    return render(request, template_name, context)


class ContestResultView(DetailView):
    """Страница конкурса с описанием."""

    model = Contest
    template_name = 'contests/contest_result.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты голосования'
        return context


def contest_error(request):
    """Страница ошибки если нет доступных конкурсов."""

    template = 'contests/contest_error.html'
    return render(request, template)
