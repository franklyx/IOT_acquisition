#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Celery Basic Setting
"""
from __future__ import absolute_import
from kombu import Queue
from tools.cfgparser import parser


BROKER_URL = 'redis://:' + parser.rpass + '@' + parser.rhost + ':' + parser.rport + '/12'
CELERY_RESULT_BACKEND = 'redis://:' + parser.rpass + '@' + parser.rhost + ':' + parser.rport + '/13'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True
BROKER_TRANSPORT_OPTIONS = {'fanout_prefix': True}
CELERY_DEFAULT_QUEUE = 'operate'
CELERY_DEFAULT_EXCHANGE = 'operate'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'operate.default'

CELERY_QUEUES = (
    Queue('operate', routing_key='operate.#'),
    Queue('mongodb', routing_key='mongodb.#'),
)

CELERY_ROUTES = {
    'schedule.consumer.tasks.data_type': {
        'queue': 'operate',
        'routing_key': 'operate.check',
    },
    'schedule.consumer.tasks.record_to_mongodb': {
        'queue': 'mongodb',
        'routing_key': 'mongodb.insert',
    }
}
