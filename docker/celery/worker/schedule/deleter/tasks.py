#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# MQTT Publisher
# Crontab task, delete data from mongodb cache regularly, then send to MQTT.
"""
from __future__ import absolute_import

import datetime
import time
import traceback
from bson.objectid import ObjectId
from model.mongodb import get_latest_seqid, remove_cache
from model.cfgparser import parser
from celery import shared_task


@shared_task(bind=True, max_retries=2, default_retry_delay=5)
def deleter(self):
    """
    :return: Void
    ：function: delete the older cache data in mongodb regularly.
    """
    try:
        seqid = get_latest_seqid()
        piece = ObjectId().__str__()[8:]
        delta = datetime.datetime.utcnow() - datetime.timedelta(days=int(parser.delete_cache))
        stamp = hex(int(time.mktime(delta.timetuple())))[2:]
        newid = stamp+piece
        if newid >= seqid:
            return
        else:
            remove_cache(newid)
    except Exception as exc:
        # logger.error(traceback.format_exc())
        traceback.print_exc()
        raise self.retry(exc=exc)


if __name__ == "__main__":
    deleter()
