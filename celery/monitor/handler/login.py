#!/usr/bin/env python
# -*-coding:utf-8 -*-

import tornado.web

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/index")
