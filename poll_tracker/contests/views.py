from django.shortcuts import render


def contests_list(request):
    """Страница со списком конкурсов."""

    template = 'contests/contest_list.html'
    context = {
        'title': 'Список конкурсов',
    }
    return render(request, template, context)


def contest_detail(request, contest_id: int):
    """Страница конкурса с описанием."""

    template = 'contests/contest_detail.html'
    context = {
        'title': f'Описание конкурса',
        'contest': contest_id,
    }
    return render(request, template, context)


def contest_result(request, contest_id):
    """Страница результатов конкурса."""

    template = 'contests/contest_result.html'
    context = {
        'title': f'Результаты голосования',
        'contest': contest_id,
    }
    return render(request, template, context)


def contest_stage(request, contest_id, contest_track_id, stage_id):
    """Страница голосования."""

    template = 'contests/contest_stage.html'
    context = {
        'title': f'Страница голосования',
        'contest': contest_id,
        'track': contest_track_id,
        'stage': stage_id,
    }
    return render(request, template, context)


def contest_error(request):
    """Страница ошибки."""

    template = 'contests/contest_error.html'
    context = {
        'title': 'Страница временно не доступна',
    }
    return render(request, template, context)
