from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.conf import settings
import os.path
admin.autodiscover()
import staticmedia

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

urlpatterns = patterns(
    '',
    (r'^$', 'antisocial.main.views.index'),
    (r'^subscriptions/$', 'antisocial.main.views.subscriptions'),
    (r'^subscriptions/(?P<id>\d+)/$', 'antisocial.main.views.subscription'),
    (r'^subscriptions/(?P<id>\d+)/mark_read/$',
     'antisocial.main.views.subscription_mark_read'),
    (r'^subscriptions/add/$', 'antisocial.main.views.add_subscription'),
    (r'^subscriptions/import/$', 'antisocial.main.views.import_feeds'),
    (r'^accounts/', include('userena.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'smoketest/', include('smoketest.urls')),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
) + staticmedia.serve()
