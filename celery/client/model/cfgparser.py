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

    # Consumer
    chost = cf.get("consumer", "host")
    cport = cf.get("consumer", "port")
    cuser = cf.get("consumer", "username")
    cpass = cf.get("consumer", "password")
    ckeepalive = cf.get("consumer", "keepalive")
    ctopic = cf.get("consumer", "topic")
    # client_id
    is_not_existed = "client_id" not in cf.options("consumer")
    if is_not_existed:
        client_id = ObjectId().__str__()
        cf.set("consumer", "client_id", client_id)
        with open("config/main.conf", 'w') as f:
            cf.write(f)
    else:
        client_id = cf.get("consumer", "client_id")

    # Publisher
    phost = cf.get("publisher", "host")
    pport = cf.get("publisher", "port")
    puser = cf.get("publisher", "username")
    ppass = cf.get("publisher", "password")
    pkeepalive = cf.get("publisher", "keepalive")
    ptopic = cf.get("publisher", "topic")

    # Redis
    rhost = cf.get("redis", "host")
    rport = cf.get("redis", "port")
    rpass = cf.get("redis", "password")

    # API
    alarm_url = cf.get("api", "alarm_url")

    # Periodic
    delete_cache = cf.get("periodic", "delete_cache_periodic")
    publish_cache = cf.get("periodic", "publish_cache_periodic")
