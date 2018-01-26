#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Celery Task App
# pre-process device date, then insert to mongodb and redis.
"""
from __future__ import absolute_import

import copy
import datetime
import json
import traceback

import jsonschema
import requests
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
from model.cfgparser import parser
from model.convert import checker
from model.error import FactoryMissingError, DeviceMissingError
from model.pyredis import rcon
from celery import shared_task
from celery.utils.log import get_task_logger

# init logger
logger = get_task_logger(__name__)

# Mongodb Connector
uri = "mongodb://%s:%s@%s:%s/admin?authMechanism=MONGODB-CR" % (parser.muser, parser.mpass, parser.mhost, parser.mport)
conn = MongoClient(uri, connect=False)

# Json Schema
with open("config/schema.json", "r") as json_file:
    json_schema = json.load(json_file)


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def record_to_mongodb(self, is_alarm, payload):
    """
    :param self: instance
    :param is_alarm: [number]optional 0(normal)、1(alarm)
    :param payload: [object]The Original Json Object
    :return: The Input parameter 'payload'
    """
    item = copy.deepcopy(payload)  # ensure that the param 'payload' won't be changed
    result1, result2, collection1, collection2 = None, None, None, None
    try:
        device_id = item["ManufacturingCode"]
        item["_id"] = ObjectId().__str__()
        item["Timestamp"] = datetime.datetime.strptime(item["Timestamp"], "%Y-%m-%d %H:%M:%S")

        # insert to product database
        db = rcon.get("factory_id")
        table = device_id+"_alarm" if is_alarm else device_id
        is_existed = rcon.hexists(device_id + "_alarm", "start_id")
        if is_alarm and not is_existed:
            rcon.hset(device_id + "_alarm", "start_id", item["_id"])
            rcon.hset(device_id + "_alarm", "start_time", payload["Timestamp"])
        if not is_alarm and is_existed:
            rcon.hdel(device_id + "_alarm", "start_id", "start_time")
        collection1 = conn[db][table]
        collection2 = conn.message_cache.bin_log
        result1 = collection1.insert(item)
        collection1.ensure_index([("Timestamp", 1)], backgroud=True)

        # insert to message_cache database
        version = {"_id": ObjectId().__str__(), "db": db, "table": table, "action": "insert",
                   "type": is_alarm, "para": dumps([item])}
        result2 = collection2.insert(version)
        return payload
    except Exception, exc:
        traceback.print_exc()
        if result1 and not result2:
            collection1.remove(item)
        # retry again
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def record_to_redis(self, item):
    """
    :param self: instance
    :param item: [object]The Original Json Object
    :return: [Object]The Input parameter 'item'
    """
    try:
        device_id = item["ManufacturingCode"]
        item = json.dumps(item)
        rcon.set(device_id, item)
        return item
    except Exception, exc:
        traceback.print_exc()
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def exist_device(self, item):
    """
    :param self: instance
    :param item: [object]The Original Json Object
    :return: [Object]The Input parameter 'item'
    """
    try:
        factory_id = rcon.get("factory_id")
        if not factory_id:
            collection = conn.factory.factory
            factory = collection.find_one()
            if not factory:
                raise FactoryMissingError
            rcon.set("factory_id", factory["_id"])
            factory_id = factory["_id"]

        device_id = item["ManufacturingCode"]
        if not rcon.sismember("devices", device_id):
            conn[factory_id].equipment.ensure_index([("factory_number", 1)], backgroud=True, unique=True)
            device = conn[factory_id].equipment.find_one({"factory_number": device_id})
            if not device:
                raise DeviceMissingError
            rcon.sadd("devices", device_id)

        return item
    except Exception as exc:
        traceback.print_exc()
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def data_type(self, item):
    """
    :param self: instance
    :param item: [object]The Original Json Object
    :return: [Object]The Input parameter 'item'
    """
    try:
        oc_alarm = item.get("OCAlarm")
        ov_alarm = item.get("OVAlarm")
        alarm_code = item.get("AlarmCode", "")
        expression = oc_alarm or ov_alarm or alarm_code
        flag = 1 if expression else 0
        try:
            if flag:
                resp = requests.post(parser.alarm_url, data={"alarm_data": dumps(item)}, timeout=15.0)
                resp.raise_for_status()
        except Exception as exc:
            traceback.print_exc()
        finally:
            return flag
    except Exception, exc:
        traceback.print_exc()
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def normalize(self, item):
    """
    :param self: instance
    :param item: [object]The Original Json Object
    :return: [Object]The Input parameter 'item'
    """
    try:
        jsonschema.validate(item, json_schema,  format_checker=checker)
        return item
    except Exception, exc:
        # logger.exception(traceback.format_exc())
        traceback.print_exc()
        raise self.retry(exc=exc)
