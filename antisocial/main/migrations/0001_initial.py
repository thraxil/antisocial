# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=256, db_index=True)),
                ('title', models.CharField(max_length=256)),
                ('link', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('author', models.CharField(max_length=256)),
                ('published', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('guid', models.CharField(max_length=256, db_index=True)),
                ('title', models.CharField(max_length=256)),
                ('last_fetched', models.DateTimeField(null=True)),
                ('last_failed', models.DateTimeField(null=True)),
                ('next_fetch', models.DateTimeField()),
                ('backoff', models.IntegerField(default=0)),
                ('etag', models.CharField(default=b'', max_length=256)),
                ('modified', models.CharField(default=b'', max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed', models.ForeignKey(to='main.Feed')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('entry', models.ForeignKey(to='main.Entry')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entry',
            name='feed',
            field=models.ForeignKey(to='main.Feed'),
            preserve_default=True,
        ),
    ]
