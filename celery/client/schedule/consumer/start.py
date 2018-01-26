#!/usr/bin/env python
# -*-coding:utf-8 -*-


import json
import traceback
import paho.mqtt.client as mqtt

from model.cfgparser import parser
from schedule.consumer.tasks import normalize, exist_device, data_type, record_to_mongodb, record_to_redis


# EMQTT Connector
client = mqtt.Client(parser.client_id, clean_session=False)
client.username_pw_set(parser.cuser, parser.cpass)


def on_connect(client, userdata, flags, rc):
    # '+': match one step，'#'：match all children stop
    print "Connected with result code " + str(rc)
    client.subscribe(parser.ctopic, qos=2)


def on_message(client, userdata, msg):
    try:
        print msg.topic + " " + str(msg.payload)
        payload = json.loads(msg.payload)
        chain = (normalize.s(payload) | exist_device.s() | data_type.s() |
                 record_to_mongodb.s(payload) | record_to_redis.s())
        chain.apply_async(queue="default")
    except Exception as exc:
        traceback.print_exc()


def consumer():
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(parser.chost, port=int(parser.cport), keepalive=int(parser.ckeepalive))
        client.loop_forever()
    except Exception as exc:
        traceback.print_exc()


if __name__ == "__main__":
    consumer()
