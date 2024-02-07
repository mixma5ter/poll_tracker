import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from scores.models import Score
from users.models import Contestant
from .models import Question


def get_client_ip(request):
    """Получение IP адреса из запроса."""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_current_question(request):
    """Получение текущего вопроса."""

    question = Question.objects.filter(is_active=True).first()

    if question:
        response = {
            'text': question.text,
            'options': question.options,
        }
    else:
        # возвращаем заглушку
        response = {
            'text': 'Нет активных вопросов',
        }

    return JsonResponse(response)


def submit_answer(request):
    """Обработка ответа на вопрос."""

    contestant_ip = get_client_ip(request)
    contestant = get_object_or_404(Contestant, ip_address=contestant_ip)  # Получаем участника по IP-адресу

    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        answer = body['answer']

        # получаем вопрос из активного конкурса этапа брейн-ринг
        question = Question.objects.filter(
            stages__contest__is_active=True,
            stages__type='brain_ring',
            is_active=True
        ).first()

        correct_answer = question.correct_answer

        score = Score.objects.filter(
            contest__is_active=True,
            question=question,
            contestant=contestant
        ).first()

        if answer == correct_answer:
            score.score = question.points  # Ставим оценку за верный ответ
            score.save()
        else:
            score.score = 0  # Ставим оценку 0 за неверный ответ
            score.save()

        return JsonResponse({'success': True})

    except KeyError:
        return JsonResponse({'success': False})


def brain_ring_page(request):
    """Страница с вопросом."""
    return render(request, 'brainring/brainring.html')
