import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from app.user.models import User


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        if User.objects.count() == 0:
            admin = User.objects.create_superuser(
                username=settings.DJANGO_ADMIN_NAME,
                password=settings.DJANGO_ADMIN_PASSWORD,
                email=settings.DJANGO_ADMIN_EMAIL,
            )
            admin.save()
        else:
            logger.warning('Admin account can only be initialized if no users exist')
