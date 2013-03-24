from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from datetime import datetime
from django.utils.timezone import utc
from .models import Feed


@task
def process_feed(feed_id):
    f = Feed.objects.get(id=feed_id)
    f.fetch()


@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def schedule_feeds():
    """ find all the feeds that are scheduled for fetching
    and add them to the queue """
    now = datetime.utcnow().replace(tzinfo=utc)
    for f in Feed.objects.filter(
            next_fetch__lt=now).order_by("next_fetch"):
        process_feed.delay(f.id)
