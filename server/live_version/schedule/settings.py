#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Celery Basic Setting
"""
from __future__ import absolute_import, print_function
from datetime import timedelta
from kombu import Queue
from celery.schedules import crontab
from tools.cfgparser import parser


BROKER_URL = 'redis://:' + parser.rpass + '@' + parser.rhost + ':' + parser.rport + '/10'
CELERY_RESULT_BACKEND = 'redis://:' + parser.rpass + '@' + parser.rhost + ':' + parser.rport + '/11'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = False
CELERY_IGNORE_RESULT = True
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'task.default'

CELERY_QUEUES = (
    Queue('default', routing_key='task.#'),
    Queue('crontab', routing_key='regular.#'),
)

CELERY_ROUTES = {
    'schedule.publisher.tasks.publisher': {
        'queue': 'crontab',
        'routing_key': 'regular.publish',
    },
    'schedule.deleter.tasks.deleter': {
        'queue': 'crontab',
        'routing_key': 'regular.delete',
    },
    'schedule.reporter.tasks.main': {
        'queue': 'crontab',
        'routing_key': 'regular.main',
    }
}

CELERYBEAT_SCHEDULE = {
    'publish-every-5-minutes': {
        'task': 'schedule.publisher.tasks.publisher',
        'schedule': timedelta(minutes=int(parser.publish_cache)),
        #'schedule': timedelta(seconds=300),
        'args': ()
    },
    'delete-every-5-day': {
        'task': 'schedule.deleter.tasks.deleter',
        'schedule': timedelta(days=int(parser.delete_cache)),
        'args': ()
    }
    #'production-intermediate-table': {
    #    'task': 'schedule.reporter.tasks.main',
    #    'schedule': crontab(minute=0, hour=0),  # 凌晨执行一次
    #    'args': ()  # 传给Task的参数
    #}
}
