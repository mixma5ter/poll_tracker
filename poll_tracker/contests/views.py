from django.db.models import Count, Sum
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from contests.models import Contest, Stage, Track
from scores.models import Score
from scores.tables import ResultTable
from users.models import Judge


class IndexView(View):
    """Главная страница с регистрацией."""

    template_name = 'contests/index.html'
    title = 'Регистрация'
    description = 'Для участия в конкурсе необходимо зарегистрироваться в качестве судьи.\n\n' \
                  'Для этого выберете своё имя из списка ниже.'
    button_text = 'Выберете своё имя'

    def get(self, request):
        contests = Contest.objects.filter(is_active=True)
        tracks = Track.objects.filter(contest__in=contests)
        judges = Judge.objects.filter(tracks__in=tracks).distinct()
        if not judges:
            raise Http404

        context = {
            'title': self.title,
            'description': self.description,
            'button_text': self.button_text,
            'judges': judges,
        }

        return render(request, self.template_name, context)


class ContestsListView(ListView):
    """Страница со списком конкурсов."""

    template_name = 'contests/contest_list.html'
    context_object_name = 'contests'

    def get_queryset(self):
        contests = Contest.objects.filter(is_active=True)
        return contests.order_by('-start_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Конкурсы'
        context['judge_slug'] = self.kwargs['judge_slug']
        context['judge_name'] = Judge.objects.get(slug=self.kwargs['judge_slug'])
        context['breadcrumbs'] = [
            ['/', 'Главная'],
            ['', 'Конкурсы'],
        ]
        return context


class ContestDetailView(DetailView):
    """Страница конкурса с описанием."""

    model = Contest
    template_name = 'contests/contest_detail.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Описание конкурса'
        context['judge_slug'] = self.kwargs['judge_slug']
        context['judge_name'] = Judge.objects.get(slug=self.kwargs['judge_slug'])
        context['tracks'] = self.get_object().tracks.all().order_by('pub_date')
        context['breadcrumbs'] = [
            ['/', 'Главная'],
            [f'/contests/{self.kwargs["judge_slug"]}/', 'Конкурсы'],
            ['', f'{self.get_object()}'],
        ]
        return context


class ContestStageView(DetailView):
    """Страница выбора этапа конкурса."""

    model = Contest
    template_name = 'contests/contest_stage.html'
    context_object_name = 'contest'
    pk_url_kwarg = 'contest_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Этапы конкурса'
        track = Track.objects.get(pk=self.kwargs['track_pk'])
        context['track'] = track
        context['stages'] = self.get_object().stages.all()
        context['judge_slug'] = self.kwargs['judge_slug']
        context['judge_name'] = Judge.objects.get(slug=self.kwargs['judge_slug'])
        context['breadcrumbs'] = [
            ['/', 'Главная'],
            [f'/contests/{self.kwargs["judge_slug"]}/', 'Конкурсы'],
            [f'/contests/{self.kwargs["judge_slug"]}/{self.kwargs["contest_pk"]}',
             f'{self.get_object()}'],
            ['', f'{track}'],
        ]
        return context


def add_score_view(request, judge_slug: str, contest_pk: int, track_pk: int, stage_pk: int):
    """Страница голосования."""

    title = 'Голосование'
    description = 'Проголосуйте за участника, затем нажмите "Подтвердить выбор"'
    button_text = 'Подтвердить выбор'
    template_name = 'contests/contest_polling.html'

    contest = Contest.objects.get(pk=contest_pk)
    track = Track.objects.get(pk=track_pk)
    stage = Stage.objects.get(pk=stage_pk)
    contestants = track.contestants.select_related()
    criterias = stage.criterias.select_related()
    data = contest.scores.all().filter(
        judge__slug=judge_slug).filter(
        track__pk=track_pk).filter(
        stage__pk=stage_pk).filter(
        contestant__in=contestants).filter(
        criteria__in=criterias)

    ScoreFormset = modelformset_factory(
        Score,
        fields=(
            'id',
            'score',
        ),
        extra=0,
    )

    if request.method == 'POST':
        formset = ScoreFormset(request.POST, queryset=data)
        if formset.is_valid():
            for form in formset:
                score = form.save(commit=False)
                score.contest_id = contest_pk
                score.track_id = track_pk
                score.stage_id = stage_pk
                score.save()
    else:
        formset = ScoreFormset(queryset=data)

    breadcrumbs = [
        ['/', 'Главная'],
        [f'/contests/{judge_slug}/', 'Конкурсы'],
        [f'/contests/{judge_slug}/{contest_pk}', contest],
        [f'/contests/{judge_slug}/{contest_pk}/{track_pk}', track],
        ['', f'{stage.title}'],
    ]

    context = {
        'title': title,
        'description': description,
        'button_text': button_text,
        'stage': stage.title,
        'criterias': criterias,
        'contestants': contestants,
        'formset': formset,
        'judge_name': Judge.objects.get(slug=judge_slug),
        'breadcrumbs': breadcrumbs,
    }

    if len(formset) > 0:
        return render(request, template_name, context)

    raise Http404


def results_view(request, judge_slug: str, contest_pk: int):
    """Страница результатов конкурса."""

    title = 'Результаты'
    template_name = 'contests/contest_polling.html'

    contest = Contest.objects.get(pk=contest_pk)
    data = contest.scores.values('contestant__name').annotate(Sum('score'))
    table = ResultTable(data)

    breadcrumbs = [
        ['/', 'Главная'],
        [f'/contests/{judge_slug}/', 'Конкурсы'],
        [f'/contests/{judge_slug}/{contest_pk}', contest],
        ['', f'Голосование'],
    ]

    context = {
        'title': title,
        'table': table,
        'judge_name': Judge.objects.get(slug=judge_slug),
        'breadcrumbs': breadcrumbs,
    }

    return render(request, template_name, context)


def contest_error(request):
    """Страница ошибки если нет доступных конкурсов."""

    template = 'contests/contest_is_not_active.html'
    return render(request, template)
