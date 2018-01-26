#!/usr/bin/env python
# coding:utf-8

import time
import random
import json
import datetime
import paho.mqtt.client as mqtt

"""EMQTT消息发送端"""
"""单线程顺序发送"""

device_ids = ["782ABC292323"]

class SendMqtt:
    def __init__(self):
        device_id = random.sample(device_ids, 1)[0]
        TIME = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        self.data = {
            "Timestamp": TIME,
            "ManufacturingCode": device_id,
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
            "OCAlarm": random.randint(0, 1),
            "OVAlarm": 0,
            "AlarmCode": "",
        }

        "MQTT服务器配置"
        self.server = "10.9.40.15"
        self.port = "1883"
        self.username = "admin"
        self.password = "admin"
        self.queue = "/devices/"+device_id

    def send(self, message):
        "发送消息至MQTT服务器"
        mqttc = mqtt.Client()
        mqttc.username_pw_set(self.username, self.password)
        mqttc.connect(self.server, self.port, keepalive=60)
        mqttc.publish(self.queue, message)

    def message(self):
        "定义需要发送的内容"
        message = json.dumps(self.data)
        self.send(message)


if __name__ == "__main__":
    while True:
        Send = SendMqtt()
        Send.message()
        time.sleep(5)
