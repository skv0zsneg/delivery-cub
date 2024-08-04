from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользователь"""

    balance = models.DecimalField(
        default=0,
        verbose_name="баланс",
        decimal_places=2,
        max_digits=12,
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
