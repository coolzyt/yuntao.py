#!/usr/bin/env python
#coding=utf8
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado import web
from yuntao import log
from yuntao import dao
import business.crawler.rssreader
import threading
def main():
    #dao.init("127.0.0.1","yuntao",user="root",password="root",poolsize=5);
    import os
    tornado.options.parse_command_line()
    static_path = os.path.join(os.path.dirname(__file__),"./pages/")
    application = tornado.web.Application([
        (r"/pages/rssreader",business.crawler.rssreader.RssReader),
		(r"/pages/(.*)", web.StaticFileHandler, {"path": static_path}), #只是为了本地调试用
    ],thread_mode=True,thread_num=200)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80,address="127.0.0.1")
    log.info("Server start at %d",80)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
