from django.shortcuts import render


def contests_list(request):
    """Страница со списком конкурсов."""

    template = 'contests/contests_list.html'
    return render(request, template)


def contest_detail(request, contest_id: int):
    """Страница конкурса с рписанием."""

    template = 'contests/contest_detail.html'
    context = {
        'contest': contest_id,
    }
    return render(request, template, context)


def contest_result(request, contest_id):
    """Страница результатов конкурса."""

    template = 'contests/contest_result.html'
    context = {
        'contest': contest_id,
    }
    return render(request, template, context)


def contest_stage(request, contest_id, contest_track_id, stage_id):
    """Страница с результатами."""

    template = 'contests/contest_stage.html'
    context = {
        'contest': contest_id,
        'track': contest_track_id,
        'stage': stage_id,
    }
    return render(request, template, context)


def contest_error(request):
    """Страница ошибки."""

    template = 'contests/contest_error.html'
    return render(request, template)
