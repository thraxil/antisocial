from django.test import TestCase
from antisocial.main.models import Feed
from datetime import datetime, timedelta


def feed_factory():
    return Feed(
        url="http://example.com/",
        guid="1234",
        title="test feed",
        last_fetched=datetime.now(),
        last_failed=datetime.now(),
        next_fetch=datetime.now() + timedelta(hours=1)
    )


class DummyFeed(object):
    feed = dict(guid="foo")


class BasicTest(TestCase):
    def test_dummy(self):
        assert True


class TestFeed(TestCase):
    def test_try_fetch(self):
        f = feed_factory()
        f.try_fetch()
        self.assertEqual(f.backoff, 0)

    def test_update_guid(self):
        f = feed_factory()
        f.update_guid(DummyFeed())
        self.assertEqual(f.guid, "foo")
