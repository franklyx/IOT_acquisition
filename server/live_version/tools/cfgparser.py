#!/usr/bin/env python
# -*-coding:utf-8 -*-

import ConfigParser
from bson.objectid import ObjectId


class parser:
    cf = ConfigParser.ConfigParser()
    cf.read("config/main.conf")

    # Default
    my_ip = cf.get("default", "my_ip")

    # factoryId
    if "factoryid" not in cf.options("default"):
        factoryid = ObjectId().__str__()
        cf.set("default", "factoryid", factoryid)
        with open("config/main.conf", 'w') as f:
            cf.write(f)
    else:
        factoryid = cf.get("default", "factoryid")

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
    keepalive = cf.get("mqtt", "keepalive")
    consumer_topic = cf.get("mqtt", "consumer_topic")
    publisher_topic = cf.get("mqtt", "publisher_topic")
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
    rdb = cf.get("redis", "db")

    # API
    alarm_url = cf.get("api", "alarm_url")

    # TOKEN
    secret_key_token = cf.get('token', 'secret_key_token')
    secret_key_rf_token = cf.get('token', 'secret_key_token')
    auth_salt = cf.get('token', 'auth_salt')

    # Periodic
    delete_cache = cf.get("periodic", "delete_cache_periodic")
    publish_cache = cf.get("periodic", "publish_cache_periodic")
