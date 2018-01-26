#!/usr/bin/env python
# -*-coding:utf-8 -*-

from handler.login import HomeHandler
from handler.index import IndexHandler

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = [
    (r"/", HomeHandler),
    (r"/index", IndexHandler)
]
