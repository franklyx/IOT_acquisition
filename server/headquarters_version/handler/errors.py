#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
handler.errors
~~~~~~~~~~~~~~

定义错误返回的字典

"""

status_0 = dict(status_code=405, reason='Method not allowed.')
status_1 = dict(status_code=404, reason='API not found.')
status_21 = dict(status_code=400, reason='Messing token.')
status_22 = dict(status_code=400, reason='Messing params.')
status_23 = dict(status_code=401, reason='Wrong password.')
status_24 = dict(status_code=404, reason='Resource not found.')
status_25 = dict(status_code=401, reason='Wrong token.')
status_26 = dict(status_code=401, reason='Wrong username.')
status_27 = dict(status_code=400, reason='Messing rf-token.')
status_28 = dict(status_code=401, reason='Wrong rf-token.')
status_29 = dict(status_code=403, reason='Forbidden')
status_30 = dict(status_code=411, reason='There are subcategories under this category')
status_31 = dict(status_code=401, reason='Only allowed to build a factory')
status_32 = dict(status_code=500, reason='Server Error')
status_33 = dict(status_code=401, reason='Username already exists')
status_34 = dict(status_code=401, reason='Wrong Content-Type')
status_35 = dict(status_code=400, reason='Wrong json string')
