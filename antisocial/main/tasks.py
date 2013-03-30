from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from datetime import datetime
from django.utils.timezone import utc
import feedparser
import socket
from .models import Feed, UEntry


@task(ignore_result=True)
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


@periodic_task(run_every=crontab(hour="*", minute="*/5", day_of_week="*"))
def expunge_uentries():
    """ clear out all the uentries that have been read """
    UEntry.objects.filter(read=True).delete()


# feeds known to segfault feedparser
BLACKLIST = [
    'http://www.metrokitty.com/rss/rss.xml',
]


@task(ignore_result=True)
def add_feed(url, user=None):
    if url in BLACKLIST:
        return
    r = Feed.objects.filter(url=url)
    if r.count() > 0:
        # already have it
        if user:
            r[0].subscribe_user(user)
        return

    socket.setdefaulttimeout(5)
    # haven't seen this one before, let's fetch it
    try:
        d = feedparser.parse(url)
    except:
        socket.setdefaulttimeout(None)
        return
    guid = d.feed.get(
        'guid',
        d.feed.get(
            'id',
            d.feed.get('link', url)
        )
    )
    if 'href' in d:
        url = d.href
    socket.setdefaulttimeout(None)
    now = datetime.utcnow().replace(tzinfo=utc)
    f = Feed.objects.create(
        url=url,
        title=d.feed.get('title', 'no title for feed'),
        guid=guid,
        last_fetched=now,
        next_fetch=now,
    )
    if user:
        f.subscribe_user(user)
