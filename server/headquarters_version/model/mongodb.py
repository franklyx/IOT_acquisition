#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Mongodb Operate
# include insert/remove/update/find/rollback etc operation
"""
import copy
import traceback

from pymongo import MongoClient
from exceptions import TypeError
from tools.cfgparser import parser

# Mongodb Connector
uri = "mongodb://%s:%s@%s:%s/?authMechanism=MONGODB-CR" % (parser.muser, parser.mpass, parser.mhost, parser.mport)
conn = MongoClient(uri, connect=False, maxPoolSize = 1024, minPoolSize=10)


def operate(db, table, action, para=None):
    """
    :param db: [string]DB Name
    :param table: [string]Table Name
    :param action: [string]Action Name
    :param para: [list]mongodb operation parameter
    :return: void
    """
    if not isinstance(para, list):
        raise TypeError

    collection = conn[db][table]
    result = getattr(collection, action)(*para)
    return result


def operate_with_rollback(db, table, action, para=None):
    """
    :param db: [string]DB Name
    :param table: [string]Table Name
    :param action: [string]Action Name
    :param para: [list]mongodb operation parameter
    :return: void
    """
    response, result = None, None
    try:
        response = rollback(db, table, action, para)
        result = operate(db, table, action, para)
    except Exception as exc:
        traceback.print_exc()
        if response and not result:
            response()


def rollback(db, table, action, param):
    """
    :param db: [string]DB Name
    :param table: [string]Table Name
    :param action: [string]Action Name
    :param para: [list]mongodb operation parameter
    :return: [object]rollback operation object
    """
    if not isinstance(param, list):
        raise TypeError

    collection = conn[db][table]
    para = copy.deepcopy(param)

    if action in ["insert", "insert_one", "insert_many"]:
        def response():
            collection.remove(*para)
        return response

    elif action in ["update", "update_one", "update_many"]:
        item = collection.find_one(para[0])

        def response():
            cache = {key: item[key] for key in para[1].values()[0].keys()}
            para[1] = {"$set": cache}
            collection.update(*para)
        return response

    elif action in ["remove", "delete_one", "delete_many"]:
        item = list(collection.find(para[0]))

        def response():
            collection.insert(*item)
        return response
