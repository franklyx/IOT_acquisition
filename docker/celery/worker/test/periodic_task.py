#!/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import absolute_import, print_function
from datetime import timedelta
from schedule.celery import Celery
from celery.schedules import crontab

app = Celery("periodic_task")
app.config_from_object('schedule.settings')
app.autodiscover_tasks(['schedule.publisher', 'schedule.deleter'])

app.conf.beat_schedule = {
    'publish-every-60-seconds': {
    'task': 'schedule.publisher.tasks.publisher',
    'schedule': timedelta(minutes=5),
    'args': ()
    },
    'delete-every-5-day': {
    'task': 'schedule.deleter.tasks.deleter',
    'schedule': timedelta(days=5),
    'args': ()
    }
}
app.conf.timezone = 'Asia/Shanghai'
