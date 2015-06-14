from django.conf.urls import patterns, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'antisocial.main.views.index'),
    (r'^subscriptions/$', 'antisocial.main.views.subscriptions'),
    (r'^subscriptions/(?P<id>\d+)/$', 'antisocial.main.views.subscription'),
    (r'^subscriptions/(?P<id>\d+)/mark_read/$',
     'antisocial.main.views.subscription_mark_read'),
    (r'^subscriptions/(?P<id>\d+)/fetch/$',
     'antisocial.main.views.subscription_fetch'),
    (r'^subscriptions/(?P<id>\d+)/unsubscribe/$',
     'antisocial.main.views.unsubscribe'),
    (r'^subscriptions/(?P<id>\d+)/subscribe/$',
     'antisocial.main.views.subscribe'),
    (r'^subscriptions/add/$', 'antisocial.main.views.add_subscription'),
    (r'^subscriptions/import/$', 'antisocial.main.views.import_feeds'),

    (r'api/entries/$', 'antisocial.main.views.entries'),
    (r'api/entry/(?P<id>\d+)/$', 'antisocial.main.views.entry_api'),

    (r'^accounts/', include('userena.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'smoketest/', include('smoketest.urls')),
    (r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
