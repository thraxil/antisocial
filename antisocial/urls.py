import django.views.static
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from antisocial.main.views import (
    index, subscriptions, subscription, subscription_mark_read, entries,
    unsubscribe, add_subscription, subscription_fetch, subscribe, entry_api,
    import_feeds,
)

admin.autodiscover()

urlpatterns = [
    url(r'^$', index),
    url(r'^subscriptions/$', subscriptions),
    url(r'^subscriptions/(?P<id>\d+)/$', subscription),
    url(r'^subscriptions/(?P<id>\d+)/mark_read/$', subscription_mark_read),
    url(r'^subscriptions/(?P<id>\d+)/fetch/$', subscription_fetch),
    url(r'^subscriptions/(?P<id>\d+)/unsubscribe/$', unsubscribe),
    url(r'^subscriptions/(?P<id>\d+)/subscribe/$', subscribe),
    url(r'^subscriptions/add/$', add_subscription),
    url(r'^subscriptions/import/$', import_feeds),

    url(r'api/entries/$', entries),
    url(r'api/entry/(?P<id>\d+)/$', entry_api),

    url(r'^accounts/', include('userena.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
]
