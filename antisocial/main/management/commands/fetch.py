from django.core.management.base import BaseCommand
from datetime import datetime
from django.utils.timezone import utc
from antisocial.main.models import Feed
import socket


class Command(BaseCommand):
    def handle(self, *args, **options):
        socket.setdefaulttimeout(5)
        now = datetime.utcnow().replace(tzinfo=utc)
        for f in Feed.objects.filter(next_fetch__lt=now):
#        for f in Feed.objects.all():
            print "fetching %s" % f.title
            f.fetch()
