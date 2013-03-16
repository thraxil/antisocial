from django.db import models
from django.contrib.auth.models import User
import feedparser
from datetime import datetime, timedelta
from django.utils.timezone import utc
import random


class Feed(models.Model):
    url = models.URLField()
    guid = models.CharField(max_length=256, db_index=True)
    title = models.CharField(max_length=256)
    last_fetched = models.DateTimeField(null=True)
    last_failed = models.DateTimeField(null=True)
    next_fetch = models.DateTimeField()
    backoff = models.IntegerField(default=0)

    def subscribe_user(self, user):
        r = self.subscription_set.filter(user=user)
        if r.count() == 0:
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

    def fetch(self):
        now = datetime.utcnow().replace(tzinfo=utc)
        self.last_fetched = now
        try:
            d = feedparser.parse(self.url)
            if d.feed.title != self.title:
                self.title = d.feed.title
            if d.feed.guid != self.guid:
                self.guid = d.feed.guid
            self.backoff = 0
            self.save()
            print "fetch successful"
        except:
            print "fetch failed"
            self.last_failed = now
            self.backoff = self.backoff + 1
            self.save()
        self.schedule_next_fetch()
        for entry in d.entries:
            self.update_entry(entry)

    def update_entry(self, entry):
        print "update entry"
        guid = entry.get(
            'guid',
            entry.get(
                'id',
                entry.get('link', None)
            )
        )
        if not guid:
            # no guid? can't do anything with it
            print "no guid"
            return
        print "guid: %s" % guid
        r = self.entry_set.filter(guid=guid)
        if r.count() > 0:
            # already have this one, so nothing to do
            print "already have this entry"
            return
        published = datetime.utcnow().replace(tzinfo=utc)
        if 'published' in entry:
            published = entry.published
        elif 'updated' in entry:
            published = entry.updated
        e = Entry.objects.create(
            feed=self,
            guid=guid,
            link=entry.get('link', u""),
            title=entry.get('title', u"no title"),
            description=entry.get(
                'description',
                entry.get('summary', u"")),
            author=entry.get('author', u""),
            published=published,
        )
        e.fanout()


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
        print "fanout()"
        for s in self.feed.subscription_set.all():
            print "adding uentry for %s" % s.user.username
            UEntry.objects.create(
                entry=self,
                user=s.user)


class Subscription(models.Model):
    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(User)


class UEntry(models.Model):
    entry = models.ForeignKey(Entry)
    user = models.ForeignKey(User)
    read = models.BooleanField(default=False)
