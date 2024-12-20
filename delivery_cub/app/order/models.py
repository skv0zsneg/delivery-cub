import uuid

from django.db import models

from app.common.helpers import custom_fields
from app.custom_user.models import CustomUser


class Order(models.Model):
    """Заказ"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="order",
        verbose_name="пользователь",
    )

    create_datetime = models.DateTimeField(
        verbose_name="дата и время заказа",
        auto_now_add=True,
    )

    total_price = custom_fields.CurrencyField()

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"


class OrderedDish(models.Model):
    """Заказные блюда"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="ordered_dishes",
        verbose_name="заказ",
    )

    restaurant_name = models.CharField(
        verbose_name="название ресторана",
    )

    dish_title = models.CharField(
        verbose_name="название блюда",
    )

    dish_price = custom_fields.CurrencyField()

    dish_quantity = models.PositiveIntegerField(
        verbose_name="количество блюд",
    )

    class Meta:
        verbose_name = "заказанное блюдо"
        verbose_name_plural = "заказанные блюда"
