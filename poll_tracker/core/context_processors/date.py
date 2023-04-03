from datetime import date


def year(request):
    """Добавляет переменную с текущим годом."""
    dt_now = date.today()
    return {'year': dt_now.year}


def today(request):
    """Добавляет переменную с текущей датой."""
    dt_now = date.today()
    return {'today': dt_now}
