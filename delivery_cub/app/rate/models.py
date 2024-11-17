import uuid

from django.db import models

from app.common.constants import RateMarkEnum
from app.custom_user.models import CustomUser
from app.restaurant.models import Restaurant


class Rate(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="rates",
        verbose_name="пользователь",
    )

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="rates",
        verbose_name="ресторан",
    )

    rate = models.IntegerField(
        default=RateMarkEnum.EXCELLENT.grade,
        choices=[(mark.grade, mark.description) for mark in RateMarkEnum],
        verbose_name="оценка",
    )

    comment = models.CharField(
        verbose_name="комментарий",
        blank=True,
    )

    creation_datetime = models.DateTimeField(
        verbose_name="дата и время создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
