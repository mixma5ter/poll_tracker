from django.shortcuts import render


def index(request):
    template = 'index.html'
    return render(request, template)


def contests_list(request):
    template = 'contests_list.html'
    return render(request, template)


def contest_detail(request, contest_id: int):
    template = 'contest_detail.html'
    context = {
        'contest': contest_id,
    }
    return render(request, template, context)
