#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
url
~~~

包含系统所有的路由文件
"""

from itertools import chain
from urls.token import token_handler
from urls.backend import backend_handler
from urls.fronted import fronted_handler
from urls.sys_init import init_handler
from urls.other import other_handler

handlers = list(chain(fronted_handler, backend_handler, token_handler, init_handler, other_handler))
