import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

from app.common.helpers import custom_fields
from app.restaurant.models import RestaurantDish


class CustomUser(AbstractUser):
    """Пользователь."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    balance = custom_fields.CurrencyField(
        default=Decimal(0.0),
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class CartPosition(models.Model):
    """Позиция в корзине."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cart_positions",
        verbose_name="пользователь",
    )

    dish = models.ForeignKey(
        RestaurantDish,
        on_delete=models.SET_NULL,
        related_name="cart_positions",
        verbose_name="блюдо",
        null=True,
    )

    quantity = models.PositiveIntegerField(
        verbose_name="количество",
        default=0,
    )

    class Meta:
        verbose_name = "позиция в корзине"
        verbose_name_plural = "позиции в корзине"

        constraints = (
            models.UniqueConstraint(name="unique_dish_in_cart_per_user", fields=("user", "dish")),
        )
