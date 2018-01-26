#!/usr/bin/env python
# -*-coding:utf-8 -*-

import logging
import logging.config
import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import Application
from tornado.options import define, options

define("port", default=8088, help="run on th given port", type=int)
logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger("main")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print 'Development server is running at http://IP:%s/' % options.port
    print 'Quit the server with Control-C'
    tornado.ioloop.IOLoop.instance().start()
