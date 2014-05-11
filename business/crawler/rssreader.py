#coding=utf8
import tornado
from yuntao import templates
from yuntao import log
import os
from yuntao import dao
class RssReader(tornado.web.RequestHandler):
    def get(self):
        rss.reader();
        self.write(templates.render("/pages/rssreader.html",rows=["1","2"]))
    
    