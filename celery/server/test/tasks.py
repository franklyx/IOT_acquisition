#!/usr/bin/env python
# -*- coding:utf-8-*-

"""
# Celery Task App
# pre-process factory date, then insert to mongodb and redis
"""
import copy
import json
import requests
import traceback

from bson.json_util import loads
from celery import Celery
from celery.utils.log import get_task_logger
from pyredis import rcon
from mongodb import operate
from cfgparser import parser
from convert import time2json

# Create Celery App
app = Celery('schedule')
app.config_from_object('config')
logger = get_task_logger(__name__)


@app.task(bind=True, max_retries=2, default_retry_delay=5)
def record_to_mongodb(self, item):
    """
    :param self: [object]instance itself
    :param item: [object]The Formatted Json Object
    :return: Void
    :function: insert date to mongodb server
    """
    try:
        db = item["db"]
        table = item["table"]
        action = item["action"]
        para = loads(item["para"])
        operate(db, table, action, para)
    except Exception, exc:
        traceback.print_exc()
        raise self.retry(exc=exc)


@app.task(bind=True, max_retries=2, default_retry_delay=5)
def data_type(self, payload):
    """
    :param self: [object]instance itself
    :param item: [object]The Formatted Json Object
    :return: [object]The Origin Input Json Object
    :function: pre-process factory data, then insert to redis and call the alarm api if the date type is alarm
    """
    try:
        item = copy.deepcopy(payload)
        _type = item["type"]
        if  _type in [0, 1]:
            para = loads(item["para"])[0]
            device_id = para["ManufacturingCode"]
            para = json.dumps(para, default=time2json)
            rcon.set(device_id, para)
            try:
                if _type == 0:
                    resp = requests.post(parser.alarm_url, data={"alarm_data": para, "factory_id": item["db"]}, timeout=15.0)
                    resp.raise_for_status()
            except Exception as exc:
                traceback.print_exc()
        return payload
    except Exception, exc:
        traceback.print_exc()
        raise self.retry(exc=exc)