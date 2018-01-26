#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Celery Basic Setting
"""
from datetime import timedelta

BROKER_URL = 'redis://:admin@10.9.40.117:6379/10'
CELERY_RESULT_BACKEND = 'redis://:admin@10.9.40.117:6379/11'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'

CELERY_SCHEDULE = {
    'publish-every-60-seconds': {
    'task': 'schedule.publisher.tasks.publisher',
    'schedule': timedelta(seconds=10),
    'args': ()
    },
    'delete-every-5-day': {
    'task': 'schedule.deleter.tasks.deleter',
    'schedule': timedelta(days=5),
    'args': ()
    }
}
