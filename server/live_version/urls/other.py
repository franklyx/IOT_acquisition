#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
urls.other
~~~~~~~~~~~~

未定义路径的handler
"""
from handler.basic import APINotFoundHandler

other_handler = [

    ('.*', APINotFoundHandler)

]
