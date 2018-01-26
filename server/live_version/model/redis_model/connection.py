#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
from tools.cfgparser import parser

pool = redis.ConnectionPool(host=parser.rhost, port=int(parser.rport), password=parser.rpass, db=0)
client = redis.Redis(connection_pool=pool)
