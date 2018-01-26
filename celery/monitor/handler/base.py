#!/usr/bin/env python
# -*-coding:utf-8 -*-

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Accept")

    def initialize(self):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("UserName")

    def on_finish(self):
        pass
