#!/usr/bin/env python
# -*-coding:utf-8 -*-

import traceback
import datetime
from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError

# Json Checker
checker = FormatChecker()

"""
# Json DateTime Checker
# Check whether the datetime format is correct or not.
# Returns True correctly and returns False incorrectly
"""


@checker.checks("date_string",  raises=ValidationError)
def is_valid_date(datestring):
    """
    :param datestring: [string]date_sting
    :return: Boolean
    """
    try:
        datetime.datetime.strptime(datestring, "%Y-%m-%d")
        return True
    except ValueError:
        traceback.print_exc()
        return False


@checker.checks("datetime_string",  raises=ValidationError)
def is_valid_datetime(datestring):
    """
    :param datestring: datetime_string
    :return: Boolean
    """
    try:
        datetime.datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        traceback.print_exc()
        return False


"""
# Json Encoder/Decoder Function
# encode: json.dumps(obj, default=time2json)
# decode: json.loads(json_obj, object_hook=json2time)
"""


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
