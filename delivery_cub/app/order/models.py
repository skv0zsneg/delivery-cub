from django.db import models
from django.utils import timezone

from app.user.models import User


class OrderedDish(models.Model):
    """Заказные блюда"""

    name = models.CharField(
        verbose_name="название",
    )
    price = models.DecimalField(
        verbose_name="цена",
        decimal_places=2,
        max_digits=12,
    )
    quantity = models.PositiveBigIntegerField(
        verbose_name="количество",
    )

    class Meta:
        verbose_name = "заказанное блюдо"
        verbose_name_plural = "заказанные блюда"


class Order(models.Model):
    """Заказ"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="order",
    )
    ordered_dish = models.ForeignKey(
        OrderedDish,
        on_delete=models.PROTECT,
        verbose_name="заказанные блюда",
        related_name="order",
    )
    create_datetime = models.DateTimeField(
        verbose_name="дата и время заказа",
        default=timezone.now,
    )
    total_price = models.DecimalField(
        verbose_name="стоимость заказа",
        decimal_places=2,
        max_digits=12,
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
