#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
from tools.cfgparser import parser

client = redis.Redis(host=parser.rhost, port=parser.rport, password=parser.rpass,
                     db=parser.rdb)
