from abc import ABC

from django.db.models import Func, DecimalField


class Round(Func, ABC):
    function = 'ROUND'
    arity = 2
    output_field = DecimalField()
