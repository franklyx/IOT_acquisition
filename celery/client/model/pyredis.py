#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Redis Server Connector
"""

import redis
from model.cfgparser import parser

pool = redis.ConnectionPool(host=parser.rhost, port=int(parser.rport), password=parser.rpass, db=0)
rcon = redis.Redis(connection_pool=pool)
