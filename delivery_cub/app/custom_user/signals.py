from django.db.models.signals import post_save
from django.dispatch import receiver

from app.custom_user.models import CartPosition, CustomUser


@receiver(post_save, sender=CustomUser)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        CartPosition.objects.create(user=instance)
