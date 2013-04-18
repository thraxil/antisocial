from django.db import models
from django.contrib.auth.models import User
import feedparser
from datetime import datetime, timedelta
from django.utils.timezone import utc
import random
from time import mktime
from .utils import get_feed_guid, get_entry_guid


class Feed(models.Model):
    url = models.URLField()
    guid = models.CharField(max_length=256, db_index=True)
    title = models.CharField(max_length=256)
    last_fetched = models.DateTimeField(null=True)
    last_failed = models.DateTimeField(null=True)
    next_fetch = models.DateTimeField()
    backoff = models.IntegerField(default=0)
    etag = models.CharField(max_length=256, default="")
    # store modified as a string, since we are just
    # passing it back through to feedparser
    modified = models.CharField(max_length=256, default="")

    def subscribe_user(self, user):
        r = self.subscription_set.filter(user=user)
        if r.count() < 1:
            Subscription.objects.create(
                feed=self,
                user=user,
            )
            # TODO: backfill entries

    def schedule_next_fetch(self):
        # hours to back off for failing feeds
        BACKOFF_SCHEDULE = [1, 2, 5, 10, 20, 50, 100]
        # exponentially back off failing feeds
        backoff = BACKOFF_SCHEDULE[min(self.backoff,
                                       len(BACKOFF_SCHEDULE) - 1)]
        # avoid thundering herd
        skew = random.randint(0, 60)
        delta = timedelta(hours=backoff, minutes=skew)
        now = datetime.utcnow().replace(tzinfo=utc)
        self.next_fetch = now + delta
        self.save()

    def fetch_failed(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        self.last_failed = now
        self.backoff = self.backoff + 1
        self.save()

    def try_fetch(self):
        d = feedparser.parse(self.url, etag=self.etag,
                             modified=self.modified)
        if 'status' in d and d.status == 404:
            self.fetch_failed()
            return
        if 'status' in d and d.status == 410:
            # 410 == GONE
            self.fetch_failed()
            return
        if 'entries' not in d:
            self.fetch_failed()
            return
        if 'title' in d.feed and d.feed.title != self.title:
            self.title = d.feed.title

        guid = get_feed_guid(d.feed, self.url)
        if guid != self.guid:
            self.guid = guid
        self.backoff = 0
        if 'etag' in d:
            self.etag = d.etag
        if 'modified' in d:
            self.modified = d.modified
        if 'status' in d and d.status == 301:
            self.url = d.href[:200]
        self.save()
        if 'entries' in d:
            for entry in d.entries:
                self.update_entry(entry)

    def fetch(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        if now < self.last_fetched + timedelta(minutes=15):
            # never fetch the same feed more than once per 15 minutes
            return
        self.last_fetched = now
        try:
            self.try_fetch()
        except:
            self.fetch_failed()
        self.schedule_next_fetch()

    def update_entry(self, entry):
        guid = get_entry_guid(entry)
        if not guid:
            # no guid? can't do anything with it
            return
        r = self.entry_set.filter(guid=guid[:256])
        if r.count() > 0:
            # already have this one, so nothing to do
            return
        published = datetime.utcnow().replace(tzinfo=utc)
        if 'published_parsed' in entry:
            published = datetime.fromtimestamp(
                mktime(entry.published_parsed)).replace(tzinfo=utc)
        elif 'updated_parsed' in entry:
            published = datetime.fromtimestamp(
                mktime(entry.updated_parsed)).replace(tzinfo=utc)
        try:
            e = Entry.objects.create(
                feed=self,
                guid=guid[:256],
                link=entry.get('link', u"")[:200],
                title=entry.get('title', u"no title")[:256],
                description=entry.get(
                    'description',
                    entry.get('summary', u"")),
                author=entry.get('author', u"")[:256],
                published=published,
            )
            e.fanout()
        except Exception, e:
            print str(e)

    def get_absolute_url(self):
        return "/subscriptions/%d/" % self.id


class Entry(models.Model):
    feed = models.ForeignKey(Feed)
    guid = models.CharField(max_length=256, db_index=True)
    title = models.CharField(max_length=256)
    link = models.URLField()
    description = models.TextField(blank=True)
    author = models.CharField(max_length=256)
    published = models.DateTimeField()

    def fanout(self):
        """ new entry. spread it to subscribers """
        for s in self.feed.subscription_set.all():
            UEntry.objects.create(
                entry=self,
                user=s.user)


class Subscription(models.Model):
    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(User)

    def all_entries(self):
        return UEntry.objects.filter(
            entry__feed=self.feed,
            user=self.user,
        )

    def unread_entries(self):
        return UEntry.objects.filter(
            entry__feed=self.feed,
            user=self.user,
            read=False,
        )


class UEntry(models.Model):
    entry = models.ForeignKey(Entry)
    user = models.ForeignKey(User)
    read = models.BooleanField(default=False)

    def as_dict(self):
        return dict(
            id=self.id,
            read=self.read,
            title=self.entry.title,
            link=self.entry.link,
            guid=self.entry.guid,
            description=self.entry.description,
            author=self.entry.author,
            published=str(self.entry.published)[:16],
            feed_title=self.entry.feed.title,
            feed_id=self.entry.feed.id,
        )
