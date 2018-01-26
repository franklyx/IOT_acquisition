#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os.path
import tornado.web
from url import url


class Application(tornado.web.Application):
    def __init__(self):
        handlers = url
        setting = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="a6511520-4e2e-11e6-9c97-d7e679ea6711",
            xsrf_cookies=False,
            login_url="/login",
            debug=True
            )
        super(Application, self).__init__(handlers, **setting)
