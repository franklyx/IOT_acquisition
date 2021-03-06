#!/usr/bin/env python
# -*-coding:utf-8 -*-

import ConfigParser
from bson.objectid import ObjectId


class parser:
    cf = ConfigParser.ConfigParser()
    cf.read("config/main.conf")

    # Default
    my_ip = cf.get("default", "my_ip")

    # Mongodb
    mhost = cf.get("mongodb", "host")
    mport = cf.get("mongodb", "port")
    muser = cf.get("mongodb", "username")
    mpass = cf.get("mongodb", "password")
    mdb = cf.get("mongodb", "database")

    # MQTT
    ehost = cf.get("mqtt", "host")
    eport = cf.get("mqtt", "port")
    euser = cf.get("mqtt", "username")
    epass = cf.get("mqtt", "password")
    topic = cf.get("mqtt", "topic")
    keepalive = cf.get("mqtt", "keepalive")
    # client_id
    is_not_existed = "client_id" not in cf.options("mqtt")
    if is_not_existed:
        client_id = ObjectId().__str__()
        cf.set("mqtt", "client_id", client_id)
        with open("config/main.conf", 'w') as f:
            cf.write(f)
    else:
        client_id = cf.get("mqtt", "client_id")

    # Redis
    rhost = cf.get("redis", "host")
    rport = cf.get("redis", "port")
    rpass = cf.get("redis", "password")

    # API
    alarm_url = cf.get("api", "alarm_url")