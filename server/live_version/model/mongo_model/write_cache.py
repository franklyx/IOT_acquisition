#!/usr/bin/env python
# -*-coding:utf-8 -*-

# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Mongodb Operate
# include insert/remove/update/find/rollback etc operation
"""
from bson.objectid import ObjectId
from bson.json_util import dumps
from exceptions import TypeError
from connection import client


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

    collection = client[db][table]
    result = getattr(collection, action)(*para)
    return result


def insert_cache(db, table, action, para=None, types=2):
    """
    :param db: [string]DB Name
    :param table: [string]Table Name
    :param action: [string]Action Name
    :param para: [list]mongodb operation parameter
    :param types: [number]operate type, optional: 0(normal)、1(alarm)、2(sql or others), default: 2
    :return: void
    """
    if not isinstance(para, list):
        raise TypeError

    sql = {"_id": ObjectId().__str__(), "db": db, "table": table, "action": action, "type": types,
           "para": dumps(para)}
    collection = client["message_cache"]["bin_log"]
    result = collection.insert_one(sql)
    return result
