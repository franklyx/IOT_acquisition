#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Celery Basic Setting
"""
from __future__ import absolute_import
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
CELERY_DEFAULT_QUEUE = 'operate'
CELERY_DEFAULT_EXCHANGE = 'operate'
