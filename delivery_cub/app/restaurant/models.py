from django.db import models


class Restaurant(models.Model):
    """Ресторан"""

    name = models.CharField(
        verbose_name="наименование",
        unique=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"


class Dish(models.Model):
    """Блюдо"""

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="название",
    )
    price = models.DecimalField(
        verbose_name="цена",
        decimal_places=2,
        max_digits=12,
    )

    class Meta:
        verbose_name = "блюдо"
        verbose_name_plural = "блюда"
