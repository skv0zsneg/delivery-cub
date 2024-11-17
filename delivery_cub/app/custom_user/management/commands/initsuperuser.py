import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from app.custom_user.models import CustomUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Displays current time"

    def handle(self, *args, **kwargs):
        if CustomUser.objects.count() == 0:
            admin = CustomUser.objects.create_superuser(
                username=settings.DJANGO_ADMIN_NAME,
                password=settings.DJANGO_ADMIN_PASSWORD,
                email=settings.DJANGO_ADMIN_EMAIL,
            )
            admin.save()
        else:
            logger.warning("Admin account can only be initialized if no users exist")
