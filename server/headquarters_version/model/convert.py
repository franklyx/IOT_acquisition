#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Json Encoder/Decoder Function
# encode: json.dumps(obj, default=time2json)
# decode: json.loads(json_obj, object_hook=json2time)
"""
import datetime


def time2json(obj):
    """
    :param obj: python object
    :return: json object
    """
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    else:
        return obj


def json2time(json_obj):
    """
    :param json_obj: json object
    :return: python object
    """
    if "Timestamp" in json_obj:
        result = datetime.datetime.strptime(json_obj["Timestamp"], "%Y-%m-%d %H:%M:%S")
        json_obj["Timestamp"] = result
    return json_obj
