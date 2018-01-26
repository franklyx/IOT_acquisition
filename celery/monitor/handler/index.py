#!/usr/bin/env python
# -*-coding:utf-8 -*-

import logging
from base import BaseHandler

import sys
reload(sys)
sys.setdefaultencoding('utf8')
logger = logging.getLogger("main.index")


class IndexHandler(BaseHandler):
    # @tornado.web.authenticated
    def get(self):
        print self.application.settings, self.request.host
        self.render("index.html")

    # @tornado.web.authenticated
    def post(self):
        pass
