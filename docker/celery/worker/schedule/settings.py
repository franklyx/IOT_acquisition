#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Celery Basic Setting
"""
from __future__ import absolute_import

from datetime import timedelta
from kombu import Queue
from model.cfgparser import parser

BROKER_URL = 'redis://:' + parser.rpass + '@' + parser.rhost + ':' + parser.rport + '/10'
CELERY_RESULT_BACKEND = 'redis://:' + parser.rpass + '@' + parser.rhost + ':' + parser.rport + '/11'
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
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_QUEUES = (
    Queue('default',    routing_key='task.#'),
    Queue('feed_tasks', routing_key='feed.#'),
)

CELERY_ROUTES = {
    'schedule.publisher.tasks.publisher': {
        'queue': 'feed_tasks',
        'routing_key': 'feed.publish',
    },
    'schedule.deleter.tasks.deleter': {
        'queue': 'feed_tasks',
        'routing_key': 'feed.delete',
    }
}

CELERYBEAT_SCHEDULE = {
    'publish-every-5-minutes': {
        'task': 'schedule.publisher.tasks.publisher',
        'schedule': timedelta(minutes=int(parser.publish_cache)),
        'args': ()
    },
    'delete-every-5-day': {
        'task': 'schedule.deleter.tasks.deleter',
        'schedule': timedelta(days=int(parser.delete_cache)),
        'args': ()
    }
}
