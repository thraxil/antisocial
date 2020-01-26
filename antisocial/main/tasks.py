from celery import task
from celery.decorators import periodic_task
from celery.exceptions import SoftTimeLimitExceeded
from celery.task.schedules import crontab
from datetime import datetime
from datetime import timedelta
from django.utils.timezone import utc
from django_statsd.clients import statsd
import beeline
import feedparser
import logging
import os
import socket
from .models import Feed, UEntry
from .utils import get_feed_guid
from celery.signals import worker_process_init, task_prerun, task_postrun
from django.conf import settings


@worker_process_init.connect
def initialize_honeycomb(**kwargs):
    if settings.HONEYCOMB_WRITEKEY and settings.HONEYCOMB_DATASET:
        logging.info(f'beeline initialization in process pid {os.getpid()}')
        beeline.init(
            writekey=settings.HONEYCOMB_WRITEKEY,
            dataset=settings.HONEYCOMB_DATASET,
            service_name='celery'
        )
    else:
        logging.info(f'no honeycomb settings, so skip initializing them')


@task_prerun.connect
def start_celery_trace(task_id, task, args, kwargs, **rest_args):
    queue_name = task.request.delivery_info.get("exchange", None)
    task.request.trace = beeline.start_trace(
        context={
            "name": "celery",
            "celery.task_id": task_id,
            "celery.args": args,
            "celery.kwargs": kwargs,
            "celery.task_name": task.name,
            "celery.queue": queue_name,
        }
    )


@task_postrun.connect
def end_celery_trace(task, state, **kwargs):
    beeline.add_field("celery.status", state)
    beeline.finish_trace(task.request.trace)


@task(ignore_result=True, time_limit=10, soft_time_limit=6)
def process_feed(feed_id):
    statsd.incr("process_feed")
    f = Feed.objects.get(id=feed_id)
    try:
        f.fetch()
    except SoftTimeLimitExceeded:
        f.fetch_failed()


@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def schedule_feeds():
    """ find all the feeds that are scheduled for fetching
    and add them to the queue

    sometimes the celery worker dies, but celery-beat is still
    going. then, when the worker comes back online,
    this task gets called over and over in a short time period,
    queueing up the same feeds over and over.

    we mitigate that by only adding feeds that are due in the
    last two minute window (since we normally will get called
    once per minute.) That means that feeds might get double
    added in that situation, but not 1000x added.

    But then that could correct too far the other way, and
    if celery-beat were stopped for a while, the feeds
    due in that span would never get queued back up because
    we'd miss that window. So once an hour, under normal
    operation, we make sure to queue up any due feeds,
    not just ones in the two minute window.

    """
    print("schedule_feeds()")
    statsd.incr("schedule_feeds")
    now = datetime.utcnow().replace(tzinfo=utc)
    if now.minute == 0:
        for f in Feed.objects.filter(
                next_fetch__lt=now).order_by("next_fetch"):
            process_feed.apply_async(
                args=[f.id], time_limit=10, soft_time_limit=6)
    else:
        for f in Feed.objects.filter(
            next_fetch__lt=now,
            next_fetch__gt=(
                now - timedelta(minutes=5))).order_by("next_fetch"):
            process_feed.apply_async(
                args=[f.id], time_limit=10, soft_time_limit=6)


@periodic_task(run_every=crontab(hour="*", minute="*/5", day_of_week="*"))
def expunge_uentries():
    statsd.incr("expunge_uentries")
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
            statsd.incr("duplicate_feeds")
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
    statsd.incr("add_feed")
    if url in BLACKLIST:
        return
    r = Feed.objects.filter(url=url[:200])
    if r.count() > 0:
        # already have it
        if user:
            r[0].subscribe_user(user)
        return
    initial_fetch(url)


def initial_fetch(url, user):
    # haven't seen this one before, let's fetch it
    socket.setdefaulttimeout(5)
    try:
        d = feedparser.parse(url)
    except:  # noqa: E722
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
