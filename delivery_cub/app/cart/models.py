from django.db import models

from app.restaurant.models import Dish
from app.user.models import User


class CartPosition(models.Model):
    """Позиция в корзине"""

    dish = models.OneToOneField(
        Dish,
        on_delete=models.CASCADE,
        related_name="блюдо",
        verbose_name="cart_position",
    )
    quantity = models.PositiveIntegerField(
        verbose_name="количество",
        default=1,
    )

    class Meta:
        verbose_name = "позиция в корзине"
        verbose_name_plural = "позиции в корзине"


class Cart(models.Model):
    """Корзина"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="cart",
    )
    positions = models.ForeignKey(
        CartPosition,
        on_delete=models.SET_NULL,
        verbose_name="позиция",
        related_name="cart",
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины"
