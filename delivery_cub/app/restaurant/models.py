import uuid

from django.db import models

from app.common.helpers import custom_fields


class Restaurant(models.Model):
    """Ресторан"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        verbose_name="наименование",
        unique=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"


class Dish(models.Model):
    """Блюдо"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    restaurant = models.ForeignKey(
        Restaurant,
        related_name="dishes",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name="название",
    )

    description = models.CharField(
        verbose_name="описание",
    )

    price = custom_fields.CurrencyField()

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"

        constraints = (
            models.UniqueConstraint(
                name="unique_dish_per_restaurant", fields=("restaurant", "title")
            ),
        )
