from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
import feedparser
from antisocial.main.models import Feed, Subscription, UEntry


@render_to('main/index.html')
def index(request):
    return dict(
        unread=UEntry.objects.filter(
            user=request.user,
            read=False,
        ).order_by("entry__published"))


@login_required
@render_to('main/subscriptions.html')
def subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return dict(subscriptions=subscriptions)


@login_required
def add_subscription(request):
    if request.method != "POST":
        return HttpResponseRedirect("/subscriptions/")
    url = request.POST.get('url', False)
    if not url:
        return HttpResponseRedirect("/subscriptions/")
    r = Feed.objects.filter(url=url)
    if r.count() > 0:
        r[0].subscribe_user(request.user)
        return HttpResponseRedirect("/subscriptions/")
    # haven't seen this one before, let's fetch it
    try:
        d = feedparser.parse(url)
    except Exception, e:
        return HttpResponse("error fetching feed: %s" % str(e))
    guid = d.feed.get('guid',
                      d.feed.get('id',
                                 d.feed.get('link', url)
                                 )
                      )
    f = Feed.objects.create(
        url=url,
        title=d.feed.get('title', 'no title for feed'),
        guid=guid,
        last_fetched=datetime.now(),
        next_fetch=datetime.now(),
    )
    f.subscribe_user(request.user)
    return HttpResponseRedirect("/subscriptions/")
