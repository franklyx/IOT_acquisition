#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# MQTT Publisher
# Crontab task, retrieve data from mongodb cache regularly, then send to MQTT.
"""
import datetime
import hashlib
import time
import traceback
import paho.mqtt.client as mqtt

from bson.objectid import ObjectId
from bson.json_util import dumps
from models.cfgparser import parser
from models.mongodb import get_latest_seqid, record_lastest_seqid, read_cache, remove_cache


# EMQTT Connector
client = mqtt.Client()
client.username_pw_set(parser.euser, parser.epass)
client.connect(parser.ehost, port=int(parser.eport), keepalive=int(parser.keepalive))


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


def send(payload, topic=parser.publisher_topic, qos=1, retain=True):
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

def publisher():
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


def delete():
    """
    :return: Void
    ：function: delete the older cache data in mongodb regularly.
    """
    try:
        seqid = get_latest_seqid()
        piece = ObjectId().__str__()[8:]
        delta = datetime.datetime.utcnow() - datetime.timedelta(days=5)
        stamp = hex(int(time.mktime(delta.timetuple())))[2:]
        newid = stamp+piece
        if newid >= seqid:
            return
        else:
            remove_cache(newid)
    except Exception as exc:
        # logger.error(traceback.format_exc())
        traceback.print_exc()


if __name__ == "__main__":
    while True:
        publisher()
        time.sleep(60)
