from datetime import datetime, timedelta

from django.test import TestCase
from django.utils.timezone import utc

from antisocial.main.models import Entry, Feed, extract_published


def feed_factory():
    return Feed.objects.create(
        url="http://example.com/",
        guid="1234",
        title="test feed",
        last_fetched=datetime.utcnow().replace(tzinfo=utc),
        last_failed=datetime.utcnow().replace(tzinfo=utc),
        next_fetch=datetime.utcnow().replace(tzinfo=utc) + timedelta(hours=1),
    )


def entry_factory(f):
    return Entry.objects.create(
        feed=f,
        guid="entry1234",
        title="test entry",
        link="http://example.com/entry",
        author="test author",
        published=datetime.utcnow().replace(tzinfo=utc),
    )


class DummyFeed(object):
    feed = dict(guid="foo")


class DictObj(object):
    def __init__(self, **kwargs):
        self._d = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __iter__(self):
        return iter(self._d)


class TestHelpers(TestCase):
    def test_extract_published_default(self):
        r = extract_published(dict())
        self.assertIsNotNone(r)


class TestFeed(TestCase):
    def test_try_fetch(self):
        f = feed_factory()
        f.try_fetch()
        self.assertEqual(f.backoff, 0)

    def test_update_guid(self):
        f = feed_factory()
        f.update_guid(DummyFeed())
        self.assertEqual(f.guid, "foo")

    def test_update_etag(self):
        f = feed_factory()
        d = DictObj(etag="new one")
        f.update_etag(d)
        self.assertEqual(f.etag, "new one")

    def test_update_modified(self):
        f = feed_factory()
        d = DictObj(modified="new one")
        f.update_modified(d)
        self.assertEqual(f.modified, "new one")

    def test_update_entry_already_exists(self):
        f = feed_factory()
        e = entry_factory(f)
        c = Entry.objects.count()
        f.update_entry(dict(guid=e.guid))
        # no new ones created
        self.assertEqual(c, Entry.objects.count())
