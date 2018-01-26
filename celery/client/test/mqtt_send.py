#!/usr/bin/env python
# coding:utf-8

import time
import random
import json
import datetime
import paho.mqtt.client as mqtt

"""EMQTT消息发送端"""
"""单线程顺序发送"""

device_ids = ["782ABC292321", "782ABC292322", "782ABC292323", "782ABC292324", "782ABC292325",
              "782ABC292326", "782ABC292327", "782ABC292328", "782ABC292329", "782ABC292320"
              ]

class SendMqtt:
    def __init__(self):
        device_id = random.sample(device_ids, 1)[0]
        TIME = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        self.data = {
            "Timestamp": TIME,
            "ManufacturingCode": device_id,
            "ManufacturingDate": "2016-05-30",
            "ProductModel": "NSINE03-3932-38923",
            "State": random.randint(0, 3),
            "PhaseVoltageInput": 1,
            "LineVin": round(random.uniform(200, 250), 1),
            "LineIin": round(random.uniform(100, 150), 1),
            "PhaseVinAB": round(random.uniform(300, 400), 1),
            "PhaseVinBC": round(random.uniform(300, 400), 1),
            "PhaseVinCA": round(random.uniform(300, 400), 1),
            "PhaseIinAB": 100.0,
            "PhaseIinBC": 100.0,
            "PhaseIinCA": round(random.uniform(90, 100), 1),
            "InputPower": round(random.uniform(100, 150), 1),
            "DCVout": round(random.uniform(50, 70), 1),
            "DCIout": round(random.uniform(180, 220), 1),
            "OutputPower": round(random.uniform(100, 150), 1),
            "EfficiencyRatio": round(random.uniform(0.7, 1), 2),
            "GasFlow": round(random.uniform(99, 102), 2),
            "Temperature1": round(random.uniform(80, 120), 1),
            "Temperature2": round(random.uniform(120, 500), 1),
            "OCAlarm": random.randint(0, 1),
            "OVAlarm": random.randint(0, 1),
            "AlarmCode": "",
        }

        "MQTT服务器配置"
        self.server = "10.9.40.117"
        self.port = "1883"
        self.username = "admin"
        self.password = "admin"
        self.queue = "/devices/"+device_id

    def send(self, message):
        "发送消息至MQTT服务器"
        mqttc = mqtt.Client()
        mqttc.username_pw_set(self.username, self.password)
        mqttc.connect(self.server, self.port, keepalive=60)
        mqttc.loop_start()
        mqttc.publish(self.queue, message, qos=2)
        mqttc.loop_stop()

    def message(self):
        "定义需要发送的内容"
        message = json.dumps(self.data)
        self.send(message)


if __name__ == "__main__":
    while True:
        Send = SendMqtt()
        Send.message()
        time.sleep(900)
