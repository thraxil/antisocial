from celery import task
from celery.decorators import periodic_task
from celery.exceptions import SoftTimeLimitExceeded
from celery.task.schedules import crontab
from datetime import datetime
from django.utils.timezone import utc
import feedparser
import socket
from .models import Feed, UEntry
from .utils import get_feed_guid


@task(ignore_result=True, time_limit=10)
def process_feed(feed_id):
    f = Feed.objects.get(id=feed_id)
    try:
        f.fetch()
    except SoftTimeLimitExceeded:
        f.fetch_failed()


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


@periodic_task(run_every=crontab(hour="*", minute="23", day_of_week="*"))
def remove_duplicate_feeds():
    """
    somehow, duplicate feeds occasionally show up.
    as a last resort, find them and kill them here.
    """
    guids = set()
    duplicates = []
    # order by -last_fetched means we always keep
    # the most recently fetched one when we find a duplicate
    for f in Feed.objects.all().order_by("-last_fetched"):
        if f.guid in guids:
            # we've seen it before, so it's a duplicate
            duplicates.append(f)
        guids.add(f.guid)
    for f in duplicates:
        f.delete()


# feeds known to segfault feedparser
BLACKLIST = [
    'http://www.metrokitty.com/rss/rss.xml',
]


@task(ignore_result=True)
def add_feed(url, user=None):
    if url in BLACKLIST:
        return
    r = Feed.objects.filter(url=url[:200])
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
    guid = get_feed_guid(d.feed, url)
    if 'href' in d:
        url = d.href[:200]
    socket.setdefaulttimeout(None)
    now = datetime.utcnow().replace(tzinfo=utc)
    f = Feed.objects.create(
        url=url[:200],
        title=d.feed.get('title', 'no title for feed'),
        guid=guid[:256],
        last_fetched=now,
        next_fetch=now,
    )
    if user:
        f.subscribe_user(user)
