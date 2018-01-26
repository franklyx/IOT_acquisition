#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# MQTT Publisher
# Crontab task, retrieve data from mongodb cache regularly, then send to MQTT.
"""
from __future__ import absolute_import

import hashlib
import traceback
import paho.mqtt.client as mqtt

from bson.json_util import dumps
from model.cfgparser import parser
from model.mongodb import get_latest_seqid, record_lastest_seqid, read_cache
from celery import shared_task

# EMQTT Connector
client = mqtt.Client()
client.username_pw_set(parser.puser, parser.ppass)
client.connect(parser.phost, port=int(parser.pport), keepalive=int(parser.pkeepalive))


def get_md5_value(data):
    """
    :param data: [string]string
    :return: [string]md5_code
    """
    _md5 = hashlib.md5()
    _md5.update(data)
    md5_value = _md5.hexdigest()
    return md5_value


def normalize(data):
    """
    :param data: [list]cache data
    :return: [string]Formatted Json String
    """
    payload = dict()
    payload["body"] = data
    payload["count"] = len(data)
    version = dumps(payload)
    return version


def send(payload, topic=parser.ptopic, qos=2, retain=True):
    """
    :param payload: [string]json string
    :param topic: [string]mqtt topic
    :param qos: [number]optional: 0/1/2, reliability level
    :param retain: whether retain the newest data or not when the client disconnect the mqtt server
    :return: Void
    """
    client.loop_start()
    client.publish(topic, payload, qos, retain)
    client.loop_stop()


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def publisher(self):
    """
    :return: Void
    """
    try:
        seqid = get_latest_seqid()
        data = read_cache(seqid)
        if data:
            payload = normalize(data)
            send(payload)
            record_lastest_seqid(data[-1].get('_id'))
    except Exception as exc:
        # logger.error(traceback.format_exc())
        traceback.print_exc()
        raise self.retry(exc=exc)
