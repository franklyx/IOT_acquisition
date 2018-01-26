#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Mongodb Operate
# include insert/remove/update/find/rollback etc operation
"""
import copy
import traceback

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from exceptions import TypeError
from tools.cfgparser import parser


# Mongodb Connector
uri = "mongodb://%s:%s@%s:%s/?authMechanism=MONGODB-CR" % (parser.muser, parser.mpass, parser.mhost, parser.mport)
conn = MongoClient(uri, connect=False)


# --------------- Base Function ------------------
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

    sql = {"_id": ObjectId().__str__(), "db": db, "table": table, "action": action, "type": types, "para": dumps(para)}
    collection = conn["message_cache"]["bin_log"]
    result = collection.insert_one(sql)
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


def operate_with_rollback_and_cache(db, table, action, para=None, types=2):
    """
    :param db: [string]DB Name
    :param table: [string]Table Name
    :param action: [string]Action Name
    :param para: [list]mongodb operation parameter
    :param types: [number]operate type, optional: 0(normal)、1(alarm)、2(sql or others), default: 2
    :return: void
    """
    response, result1, result2 = None, None, None
    try:
        response = rollback(db, table, action, para)
        result1 = operate(db, table, action, para)
        result2 = insert_cache(db, table, action, types, para)
    except Exception as exc:
        traceback.print_exc()
        if response and result1 and not result2:
            response()


def rollback(db, table, action, param):
    """
    :param db: [string]DB Name
    :param table: [string]Table Name
    :param action: [string]Action Name
    :param param: [list]mongodb operation parameter
    :return: void
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


# --------------- Publish Function ------------------
def get_latest_seqid(db="message_cache", table="seqId"):
    """
    :param db: [string]Cache DB Name
    :param table: [string]Table Name
    :return: [object_id_string]latest sequence id
    """
    collection = conn[db][table]
    item = list(collection.find().limit(1).sort([("_id", -1)]))
    seqid = item[0].get("seqId") if item else "000000000000000000000000"
    return seqid


def record_lastest_seqid(seqid, db="message_cache", table="seqId"):
    """
    :param seqid: [object_id_string]latest sequence id
    :param db: [string]Cache DB Name
    :param table: [string]Table Name
    :return: void
    """
    collection = conn[db][table]
    collection.insert({"_id": ObjectId().__str__(), "seqId": seqid})


def read_cache(seqid, db="message_cache", table="bin_log"):
    """
    :param seqid: [object_id_string]starting sequence id
    :param db: [string]Cache DB Name
    :param table: [string]Table Name
    :return: [list]the latest cache data
    """
    collection = conn[db][table]
    data = list(collection.find({"_id": {"$gt": seqid}})
                .limit(500)
                .sort([("_id", 1)])
                )
    return data


def remove_cache(seqid, db="message_cache", table="bin_log"):
    """
    :param seqid: [object_id_string]latest sequence id or the max removable id
    :param db: [string]Cache DB Name
    :param table: [string]Table Name
    :return: Void
    """
    conn[db][table].remove({"_id": {"$lt": seqid}})
