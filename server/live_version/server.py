#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function

import sys
import logging
import logging.config

import yaml
import tornado.web
import tornado.ioloop
import tornado.process
import tornado.netutil
import tornado.httpserver
from tornado.options import define, options

from url import handlers
from config.config import etc

reload(sys)
sys.setdefaultencoding('utf-8')

svr = tornado.web.Application(handlers=handlers, **etc)

define("port", default=7000, help="run on the given port", type=int)


def init_logger():
    filename = "config/logging.yml"
    with open(filename, "r") as f:
        config = yaml.load(f)
    logging.config.dictConfig(config)


def main():
    # init_logger()
    options.parse_command_line()
    print("Starting tornado web server on http://127.0.0.1:%s" % options.port)
    print("Quit the server with CONTROL-C")
    svr.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
    # tornado.ioloop.IOLoop.current().stop()

    # 开启多线程
    # sockets = tornado.netutil.bind_sockets(options.port)
    # tornado.process.fork_processes(2)
    # server = tornado.httpserver.HTTPServer(svr)
    # server.add_sockets(sockets)
    # tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()  
