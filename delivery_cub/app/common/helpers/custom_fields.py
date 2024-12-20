from decimal import Decimal

from django.db import models
from django.core import validators


class CurrencyField(models.DecimalField):
    default_validators = [validators.MinValueValidator(Decimal(0.0))]

    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 7
        kwargs["decimal_places"] = 2
        super().__init__(*args, **kwargs)
