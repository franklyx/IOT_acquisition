#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
mongo_model.connection
~~~~~~~~~~~~~~~~~~~~~~

连接mongodb数据库，
向外抛出mongodb数据库连接的client
"""

from pymongo import MongoClient
from tools.cfgparser import parser

db_url = "mongodb://{username}:{password}@{host}:{port}/?authMechanism=MONGODB-CR".format(
    username=parser.muser,
    password=parser.mpass,
    host=parser.mhost,
    port=parser.mport)
client = MongoClient(db_url)
