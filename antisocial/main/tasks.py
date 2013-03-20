from celery import task
from .models import Feed


@task
def process_feed(feed_id):
    f = Feed.objects.get(id=feed_id)
    f.fetch()
