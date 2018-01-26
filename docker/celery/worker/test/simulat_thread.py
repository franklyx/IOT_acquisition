#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import time
from concurrent import futures
import paho.mqtt.client as mqtt

"""EMQTT消息发送端"""
"""多线程发送"""


# 时间记录装饰器
def func_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print func.__name__, 'runtime:', time.time() - start

    return wrapper


class SendMqtt:
    def __init__(self):
        "MQTT服务器配置"
        self.server = "10.9.40.117"
        self.port = "1883"
        self.username = "admin"
        self.password = "admin"
        self.queue = "/devices/"

    def send(self, message):
        "发送消息至MQTT服务器"
        mqttc = mqtt.Client()
        mqttc.username_pw_set(self.username, self.password)
        mqttc.connect(self.server, self.port, keepalive=60)
        mqttc.publish(self.queue, message)

    def message(self, content):
        "定义需要发送的内容"
        message = json.dumps(content)
        self.send(message)


def simulation_send():
    "发送信息配置函数"
    sends = SendMqtt()
    data = {
        "Timestamp": "2017-02-21 22:30:21",
        "ManufacturingCode": "782ABC292323",
        "ManufacturingDate": "2016-05-30",
        "ProductModel": "NSINE03-3932-38923",
        "State": 2,
        "PhaseVoltageInput": 1,
        "LineVin": 220.0,
        "LineIin": 120.0,
        "PhaseVinAB": 380.0,
        "PhaseVinBC": 380.0,
        "PhaseVinCA": 380.0,
        "PhaseIinAB": 100.0,
        "PhaseIinBC": 100.0,
        "PhaseIinCA": 100.0,
        "InputPower": 120.0,
        "DCVout": 60.0,
        "DCIout": 200.0,
        "OutputPower": 120.0,
        "EfficiencyRatio": 0.89,
        "GasFlow": 100.99,
        "Temperature1": 100.0,
        "Temperature2": 100.0,
        "OCAlarm": 1,
        "OVAlarm": 1,
        "AlarmCode": "ada989128983209432"
    }
    sends.message(data)


@func_time
def loiter(n):
    "模拟需要重复执行的函数"
    executor.map(simulation_send, range(num))


if __name__ == "__main__":
    num = sys.argv[1]
    executor = futures.ThreadPoolExecutor(max_workers=3)
    loiter(num)
