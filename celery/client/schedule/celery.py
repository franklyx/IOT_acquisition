#!/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import absolute_import, print_function
from celery import Celery

# Create Celery App
app = Celery('schedule')
app.config_from_object('schedule.settings')
app.autodiscover_tasks(['schedule.consumer', 'schedule.publisher', 'schedule.deleter'], force=True)

if __name__ == '__main__':
    app.start()
