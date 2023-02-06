import socket
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import utc

from antisocial.main.models import Feed
from antisocial.main.tasks import process_feed


class Command(BaseCommand):
    def handle(self, *args, **options):
        socket.setdefaulttimeout(5)
        now = datetime.utcnow().replace(tzinfo=utc)
        for f in Feed.objects.filter(next_fetch__lt=now).order_by(
            "next_fetch"
        ):
            process_feed.delay(f.id)
