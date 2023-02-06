import django.views.static
from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path

from antisocial.main.views import (add_subscription, entries, entry_api,
                                   import_feeds, index, subscribe,
                                   subscription, subscription_fetch,
                                   subscription_mark_read, subscriptions,
                                   unsubscribe)

admin.autodiscover()

urlpatterns = [
    re_path(r"^$", index),
    re_path(r"^subscriptions/$", subscriptions),
    re_path(r"^subscriptions/(?P<id>\d+)/$", subscription),
    re_path(r"^subscriptions/(?P<id>\d+)/mark_read/$", subscription_mark_read),
    re_path(r"^subscriptions/(?P<id>\d+)/fetch/$", subscription_fetch),
    re_path(r"^subscriptions/(?P<id>\d+)/unsubscribe/$", unsubscribe),
    re_path(r"^subscriptions/(?P<id>\d+)/subscribe/$", subscribe),
    re_path(r"^subscriptions/add/$", add_subscription),
    re_path(r"^subscriptions/import/$", import_feeds),
    re_path(r"api/entries/$", entries),
    re_path(r"api/entry/(?P<id>\d+)/$", entry_api),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"smoketest/", include("smoketest.urls")),
    re_path(
        r"^uploads/(?P<path>.*)$",
        django.views.static.serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ]
