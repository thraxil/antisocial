from __future__ import absolute_import, unicode_literals

import logging
import os
import beeline

from celery import Celery
from celery.signals import worker_process_init, task_prerun, task_postrun
from django.conf import settings


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antisocial.settings')

app = Celery('antisocial')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@worker_process_init.connect
def initialize_honeycomb(**kwargs):
    if settings.HONEYCOMB_WRITEKEY and settings.HONEYCOMB_DATASET:
        logging.info(f'beeline initialization in process pid {os.getpid()}')
        beeline.init(
            writekey=settings.HONEYCOMB_WRITEKEY,
            dataset=settings.HONEYCOMB_DATASET,
            service_name='celery'
        )


@task_prerun.connect
def start_celery_trace(task_id, task, args, kwargs, **rest_args):
    queue_name = task.request.delivery_info.get("exchange", None)
    task.request.trace = beeline.start_trace(
        context={
            "name": "celery",
            "celery.task_id": task_id,
            "celery.args": args,
            "celery.kwargs": kwargs,
            "celery.task_name": task.name,
            "celery.queue": queue_name,
        }
    )


# optional: finish and send the trace at the end of each task
@task_postrun.connect
def end_celery_trace(task, state, **kwargs):
    beeline.add_field("celery.status", state)
    beeline.finish_trace(task.request.trace)
