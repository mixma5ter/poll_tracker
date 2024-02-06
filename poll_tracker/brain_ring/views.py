import json

from django.shortcuts import render
from django.http import JsonResponse

from .models import Question


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

    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        answer = body['answer']

        question = Question.objects.filter(is_active=True).first()
        correct_answer = question.correct_answer

        if answer == correct_answer:
            # добавить обработку ответа
            pass
        return JsonResponse({'success': True})

    except KeyError:
        return JsonResponse({'success': False})


def brain_ring_page(request):
    """Страница с вопросом."""
    return render(request, 'brainring/brainring.html')
